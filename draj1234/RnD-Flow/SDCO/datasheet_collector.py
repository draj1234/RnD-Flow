#!/usr/bin/env python3
"""
Smart Datasheet Collector & Organizer (SDCO)

A Python-based CLI tool that automatically searches and downloads datasheets
for components from a BOM, classifies them using LLM, and organizes them
into a structured folder hierarchy.

Author: AI Assistant
Version: 1.0.0
"""

import asyncio
import csv
import hashlib
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import quote_plus, urlparse

import aiofiles
import aiohttp
import click
import pandas as pd
import questionary
import yaml
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from pydantic import BaseModel
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Initialize console and logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, console=console)]
)
log = logging.getLogger("sdco")


# ============================================================================
# Data Models
# ============================================================================

class ComponentCategory(Enum):
    """Component categories for classification."""
    POWER = "Power"
    MCU_PROCESSOR = "MCU_Processor"
    MEMORY = "Memory"
    SENSORS = "Sensors"
    WIRELESS_COMMS = "Wireless_Comms"
    PASSIVES = "Passives"
    CONNECTORS = "Connectors"
    PROTECTION = "Protection"
    CLOCK_TIMING = "Clock_Timing"
    INTERFACE = "Interface"
    MECHANICAL = "Mechanical"
    REFERENCE_DOCS = "Reference_Docs"
    UNKNOWN = "Unknown"


@dataclass
class Component:
    """Represents a component from the BOM."""
    ref: str
    part_number: str
    manufacturer: str
    description: str
    quantity: int
    category: ComponentCategory = ComponentCategory.UNKNOWN
    datasheet_url: Optional[str] = None
    datasheet_path: Optional[str] = None
    download_status: str = "pending"
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DownloadResult:
    """Result of a datasheet download attempt."""
    success: bool
    url: str
    file_path: Optional[str] = None
    error: Optional[str] = None
    source: str = ""
    file_size: int = 0


@dataclass
class ManifestEntry:
    """Entry in the manifest file."""
    part_number: str
    manufacturer: str
    description: str
    category: str
    ref_designators: List[str]
    quantity: int
    datasheet_file: str
    datasheet_url: str
    download_date: str
    file_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Configuration Loader
# ============================================================================

class Config:
    """Configuration manager."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            log.warning(f"Config file {self.config_path} not found, using defaults")
            return self._default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'llm': {
                'provider': 'ollama',
                'model': 'llama3.1:8b',
                'timeout': 120,
                'temperature': 0.1
            },
            'download': {
                'max_concurrent': 5,
                'timeout': 30,
                'retries': 3,
                'retry_delay': 2
            },
            'output': {
                'base_directory': './datasheets',
                'manifest_file': 'manifest.json',
                'log_file': 'download_log.txt',
                'failed_file': 'missing_datasheets.csv'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value


# ============================================================================
# LLM Integration
# ============================================================================

class LLMClient:
    """LLM client for classification and metadata extraction."""
    
    def __init__(self, config: Config):
        self.config = config
        self.provider = config.get('llm.provider', 'ollama')
        self.model = config.get('llm.model', 'llama3.1:8b')
        self.timeout = config.get('llm.timeout', 120)
        self.temperature = config.get('llm.temperature', 0.1)
        
        if self.provider == 'openrouter':
            self.api_key = os.getenv('OPENROUTER_API_KEY')
            if not self.api_key:
                log.warning("OPENROUTER_API_KEY not set, falling back to ollama")
                self.provider = 'ollama'
    
    async def classify_component(self, component: Component) -> ComponentCategory:
        """Classify a component using LLM."""
        prompt = f"""You are an expert electronics component classifier. Classify the following component into one of these categories:
{', '.join([c.value for c in ComponentCategory if c != ComponentCategory.UNKNOWN])}

Component Information:
- Part Number: {component.part_number}
- Manufacturer: {component.manufacturer}
- Description: {component.description}

Respond with ONLY the category name (e.g., "Power", "MCU_Processor", etc.). No explanation needed."""

        try:
            if self.provider == 'ollama':
                return await self._ollama_classify(prompt)
            else:
                return await self._openrouter_classify(prompt)
        except Exception as e:
            log.warning(f"LLM classification failed for {component.part_number}: {e}")
            return self._fallback_classification(component)
    
    async def _ollama_classify(self, prompt: str) -> ComponentCategory:
        """Classify using Ollama."""
        import subprocess
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            response = result.stdout.strip()
            return self._parse_category(response)
        except FileNotFoundError:
            log.error("Ollama not found. Please install Ollama or use OpenRouter API.")
            raise
        except subprocess.TimeoutExpired:
            raise TimeoutError("Ollama request timed out")
    
    async def _openrouter_classify(self, prompt: str) -> ComponentCategory:
        """Classify using OpenRouter API."""
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            payload = {
                'model': self.config.get('llm.openrouter_model', 'meta-llama/llama-3.1-8b-instruct'),
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': self.temperature,
                'max_tokens': 20
            }
            
            async with session.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                data = await response.json()
                text = data['choices'][0]['message']['content'].strip()
                return self._parse_category(text)
    
    def _parse_category(self, text: str) -> ComponentCategory:
        """Parse category from LLM response."""
        text = text.strip().lower()
        
        category_map = {
            'power': ComponentCategory.POWER,
            'mcu_processor': ComponentCategory.MCU_PROCESSOR,
            'memory': ComponentCategory.MEMORY,
            'sensors': ComponentCategory.SENSORS,
            'wireless_comms': ComponentCategory.WIRELESS_COMMS,
            'passives': ComponentCategory.PASSIVES,
            'connectors': ComponentCategory.CONNECTORS,
            'protection': ComponentCategory.PROTECTION,
            'clock_timing': ComponentCategory.CLOCK_TIMING,
            'interface': ComponentCategory.INTERFACE,
            'mechanical': ComponentCategory.MECHANICAL,
            'reference_docs': ComponentCategory.REFERENCE_DOCS,
        }
        
        for key, category in category_map.items():
            if key in text:
                return category
        
        return ComponentCategory.UNKNOWN
    
    def _fallback_classification(self, component: Component) -> ComponentCategory:
        """Fallback keyword-based classification when LLM fails."""
        desc_lower = f"{component.manufacturer} {component.description}".lower()
        pn_lower = component.part_number.lower()
        
        # Keyword matching
        if any(kw in desc_lower for kw in ['ldo', 'regulator', 'battery', 'charger', 'pmic', 'dc-dc']):
            return ComponentCategory.POWER
        elif any(kw in desc_lower for kw in ['microcontroller', 'mcu', 'processor', 'soc', 'nrf', 'stm32']):
            return ComponentCategory.MCU_PROCESSOR
        elif any(kw in desc_lower for kw in ['flash', 'eeprom', 'ram', 'memory']):
            return ComponentCategory.MEMORY
        elif any(kw in desc_lower for kw in ['sensor', 'accelerometer', 'gyroscope', 'imu']):
            return ComponentCategory.SENSORS
        elif any(kw in desc_lower for kw in ['ble', 'bluetooth', 'wifi', 'lora', 'nfc', 'uwb', 'rf', 'wireless']):
            return ComponentCategory.WIRELESS_COMMS
        elif any(kw in desc_lower for kw in ['resistor', 'capacitor', 'inductor']):
            return ComponentCategory.PASSIVES
        elif any(kw in desc_lower for kw in ['connector', 'usb', 'header', 'jack']):
            return ComponentCategory.CONNECTORS
        elif any(kw in desc_lower for kw in ['esd', 'protection', 'tvs', 'fuse']):
            return ComponentCategory.PROTECTION
        elif any(kw in desc_lower for kw in ['crystal', 'oscillator', 'tcxo', 'clock']):
            return ComponentCategory.CLOCK_TIMING
        elif any(kw in desc_lower for kw in ['transceiver', 'buffer', 'driver', 'isolator']):
            return ComponentCategory.INTERFACE
        elif any(kw in desc_lower for kw in ['enclosure', 'mount', 'hardware']):
            return ComponentCategory.MECHANICAL
        
        return ComponentCategory.UNKNOWN
    
    async def extract_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """Extract metadata from PDF using LLM."""
        # First extract text from PDF
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                # Read first 3 pages for metadata
                for i in range(min(3, len(reader.pages))):
                    text += reader.pages[i].extract_text()
            
            # Truncate if too long
            text = text[:5000]
            
            prompt = f"""Extract the following information from this datasheet text:
- Part Number
- Manufacturer  
- Category
- Key Specifications (voltage, current, package, temperature range)
- Revision/Date

Text:
{text}

Respond in JSON format only:
{{
  "part_number": "...",
  "manufacturer": "...",
  "category": "...",
  "specifications": {{...}},
  "revision": "..."
}}
"""
            
            if self.provider == 'ollama':
                import subprocess
                result = subprocess.run(
                    ['ollama', 'run', self.model, prompt],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                response = result.stdout.strip()
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            
            return {"extracted": True, "text_length": len(text)}
            
        except Exception as e:
            log.debug(f"Metadata extraction failed: {e}")
            return {}


# ============================================================================
# Datasheet Sources
# ============================================================================

class DatasheetSource:
    """Base class for datasheet sources."""
    
    async def search(self, part_number: str, manufacturer: str) -> List[str]:
        """Search for datasheet URLs."""
        raise NotImplementedError
    
    async def download(self, url: str, save_path: str) -> DownloadResult:
        """Download datasheet from URL."""
        raise NotImplementedError


class GoogleSearch(DatasheetSource):
    """Google search with filetype:pdf filter."""
    
    async def search(self, part_number: str, manufacturer: str) -> List[str]:
        """Search Google for datasheets."""
        query = f"{part_number} {manufacturer} datasheet filetype:pdf"
        encoded_query = quote_plus(query)
        
        # Use Google Custom Search API or scrape (note: scraping violates ToS)
        # For demo purposes, we'll return a placeholder
        urls = []
        
        # Try common patterns
        manufacturers = [manufacturer, manufacturer.replace(' ', ''), 'ti', 'st', 'nxp']
        for mfr in manufacturers:
            urls.append(f"https://www.{mfr}.com/{part_number}.pdf")
        
        return urls[:5]  # Return top candidates


class ManufacturerSearch(DatasheetSource):
    """Direct manufacturer website search."""
    
    MANUFACTURER_URLS = {
        'texas instruments': 'https://www.ti.com/product/',
        'stmicroelectronics': 'https://www.st.com/en/',
        'nxp': 'https://www.nxp.com/products/',
        'analog devices': 'https://www.analog.com/en/product/',
        'infineon': 'https://www.infineon.com/cms/en/product/',
        'microchip': 'https://www.microchip.com/en-us/product/',
        'nordic semiconductor': 'https://www.nordicsemi.com/Products/',
        'murata': 'https://www.murata.com/en-us/products/',
        'yageo': 'https://www.yageo.com/en/Product/',
        'on semiconductor': 'https://www.onsemi.com/products/',
        'diodes incorporated': 'https://www.diodes.com/products/',
        'molex': 'https://www.molex.com/en-us/products/part-detail/',
        'amphenol': 'https://www.amphenol-cs.com/',
        'panasonic': 'https://na.industrial.panasonic.com/',
        'bel fuse': 'https://www.belfuse.com/products/',
    }
    
    async def search(self, part_number: str, manufacturer: str) -> List[str]:
        """Search manufacturer website."""
        urls = []
        mfr_lower = manufacturer.lower()
        
        # Find matching manufacturer URL pattern
        for mfr_key, base_url in self.MANUFACTURER_URLS.items():
            if mfr_key in mfr_lower:
                # Construct potential URLs
                urls.append(f"{base_url}{part_number}")
                urls.append(f"{base_url}{part_number.lower()}")
                break
        
        # Generic fallback
        if not urls:
            urls.append(f"https://www.google.com/search?q={quote_plus(part_number + ' datasheet')}")
        
        return urls


class DigiKeySearch(DatasheetSource):
    """Digi-Key search."""
    
    async def search(self, part_number: str, manufacturer: str) -> List[str]:
        """Search Digi-Key."""
        # Would use Digi-Key API in production
        # For now, construct URL
        url = f"https://www.digikey.com/en/products/detail/{part_number.replace('/', '-')}"
        return [url]


class MouserSearch(DatasheetSource):
    """Mouser Electronics search."""
    
    async def search(self, part_number: str, manufacturer: str) -> List[str]:
        """Search Mouser."""
        url = f"https://www.mouser.com/Search/Refine.aspx?Keyword={quote_plus(part_number)}"
        return [url]


class AllDatasheetSearch(DatasheetSource):
    """AllDatasheet.com search."""
    
    async def search(self, part_number: str, manufacturer: str) -> List[str]:
        """Search AllDatasheet."""
        url = f"https://www.alldatasheet.com/view.jsp?Searchword={part_number.upper()}"
        return [url]


# ============================================================================
# Download Manager
# ============================================================================

class DownloadManager:
    """Manages concurrent datasheet downloads."""
    
    def __init__(self, config: Config):
        self.config = config
        self.max_concurrent = config.get('download.max_concurrent', 5)
        self.timeout = config.get('download.timeout', 30)
        self.retries = config.get('download.retries', 3)
        self.retry_delay = config.get('download.retry_delay', 2)
        self.user_agents = config.get('download.user_agents', [])
        self.sources = [
            ManufacturerSearch(),
            DigiKeySearch(),
            MouserSearch(),
            GoogleSearch(),
            AllDatasheetSearch(),
        ]
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def download_url(self, url: str, save_path: str, session: aiohttp.ClientSession) -> DownloadResult:
        """Download a file from URL with retry logic."""
        try:
            headers = {
                'User-Agent': self.user_agents[0] if self.user_agents else 
                             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with session.get(url, headers=headers, timeout=self.timeout) as response:
                if response.status == 200:
                    content = await response.read()
                    
                    # Verify it's a PDF
                    if not content.startswith(b'%PDF'):
                        return DownloadResult(
                            success=False,
                            url=url,
                            error="Not a valid PDF file",
                            source=""
                        )
                    
                    # Save file
                    async with aiofiles.open(save_path, 'wb') as f:
                        await f.write(content)
                    
                    return DownloadResult(
                        success=True,
                        url=url,
                        file_path=save_path,
                        source=urlparse(url).netloc,
                        file_size=len(content)
                    )
                else:
                    return DownloadResult(
                        success=False,
                        url=url,
                        error=f"HTTP {response.status}",
                        source=""
                    )
        except asyncio.TimeoutError:
            raise  # Let retry handle it
        except Exception as e:
            return DownloadResult(
                success=False,
                url=url,
                error=str(e),
                source=""
            )
    
    async def download_for_component(self, component: Component, output_dir: Path) -> DownloadResult:
        """Try to download datasheet for a component from multiple sources."""
        for source in self.sources:
            try:
                urls = await source.search(component.part_number, component.manufacturer)
                
                async with aiohttp.ClientSession() as session:
                    for url in urls:
                        # Generate safe filename
                        safe_part = re.sub(r'[^\w\-_]', '_', component.part_number)
                        filename = f"{safe_part}_{component.manufacturer.replace(' ', '_')}.pdf"
                        save_path = output_dir / filename
                        
                        # Skip if already exists
                        if save_path.exists():
                            log.debug(f"File already exists: {save_path}")
                            continue
                        
                        result = await self.download_url(url, save_path, session)
                        if result.success:
                            return result
                
            except Exception as e:
                log.debug(f"Source {type(source).__name__} failed: {e}")
                continue
        
        return DownloadResult(
            success=False,
            url="",
            error="No datasheet found from any source",
            source=""
        )


# ============================================================================
# PDF Metadata Extractor
# ============================================================================

class PDFMetadataExtractor:
    """Extract metadata from PDF files."""
    
    def __init__(self):
        pass
    
    def extract_text(self, pdf_path: str, max_pages: int = 3) -> str:
        """Extract text from PDF."""
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for i in range(min(max_pages, len(reader.pages))):
                    text += reader.pages[i].extract_text()
            
            return text
        except Exception as e:
            log.debug(f"PDF text extraction failed: {e}")
            return ""
    
    def calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def check_duplicate(self, file_path: str, existing_files: List[str]) -> bool:
        """Check if file is a duplicate based on hash."""
        new_hash = self.calculate_hash(file_path)
        
        for existing in existing_files:
            if Path(existing).exists():
                existing_hash = self.calculate_hash(existing)
                if new_hash == existing_hash:
                    return True
        
        return False


# ============================================================================
# BOM Parser
# ============================================================================

class BOMParser:
    """Parse various BOM formats."""
    
    @staticmethod
    def parse_csv(file_path: str) -> List[Component]:
        """Parse CSV BOM file."""
        components = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                component = Component(
                    ref=row.get('Ref', ''),
                    part_number=row.get('Part Number', row.get('PartNumber', '')),
                    manufacturer=row.get('Manufacturer', ''),
                    description=row.get('Description', ''),
                    quantity=int(row.get('Quantity', '1'))
                )
                components.append(component)
        
        return components
    
    @staticmethod
    def parse_excel(file_path: str) -> List[Component]:
        """Parse Excel BOM file."""
        df = pd.read_excel(file_path)
        components = []
        
        for _, row in df.iterrows():
            component = Component(
                ref=str(row.get('Ref', '')),
                part_number=str(row.get('Part Number', row.get('PartNumber', ''))),
                manufacturer=str(row.get('Manufacturer', '')),
                description=str(row.get('Description', '')),
                quantity=int(row.get('Quantity', 1))
            )
            components.append(component)
        
        return components
    
    @staticmethod
    def parse_text(file_path: str) -> List[Component]:
        """Parse plain text BOM (one part number per line)."""
        components = []
        
        with open(file_path, 'r') as f:
            for line in f:
                part_number = line.strip()
                if part_number:
                    component = Component(
                        ref='',
                        part_number=part_number,
                        manufacturer='',
                        description='',
                        quantity=1
                    )
                    components.append(component)
        
        return components
    
    @staticmethod
    def interactive_mode() -> List[Component]:
        """Interactive mode - user enters components one by one."""
        components = []
        
        console.print("\n[bold blue]Interactive Mode[/bold blue]")
        console.print("Enter components one by one. Type 'done' when finished.\n")
        
        while True:
            part_number = questionary.text("Part Number (or 'done'): ").ask()
            if part_number and part_number.lower() == 'done':
                break
            if not part_number:
                continue
            
            manufacturer = questionary.text("Manufacturer: ").ask()
            description = questionary.text("Description: ").ask()
            quantity = questionary.text("Quantity [1]: ", default="1").ask()
            
            component = Component(
                ref='',
                part_number=part_number,
                manufacturer=manufacturer or '',
                description=description or '',
                quantity=int(quantity) if quantity.isdigit() else 1
            )
            components.append(component)
        
        return components


# ============================================================================
# Manifest Generator
# ============================================================================

class ManifestGenerator:
    """Generate and manage manifest file."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.entries: List[ManifestEntry] = []
    
    def add_entry(self, component: Component, file_path: str, file_hash: str):
        """Add entry to manifest."""
        entry = ManifestEntry(
            part_number=component.part_number,
            manufacturer=component.manufacturer,
            description=component.description,
            category=component.category.value,
            ref_designators=[component.ref] if component.ref else [],
            quantity=component.quantity,
            datasheet_file=str(file_path),
            datasheet_url=component.datasheet_url or '',
            download_date=datetime.now().isoformat(),
            file_hash=file_hash,
            metadata=component.metadata
        )
        self.entries.append(entry)
    
    def save(self, manifest_path: Optional[str] = None):
        """Save manifest to JSON file."""
        if manifest_path is None:
            manifest_path = self.output_dir / 'manifest.json'
        else:
            manifest_path = Path(manifest_path)
        
        manifest_data = {
            'generated_at': datetime.now().isoformat(),
            'total_components': len(self.entries),
            'categories': {},
            'entries': [asdict(e) for e in self.entries]
        }
        
        # Count by category
        for entry in self.entries:
            cat = entry.category
            manifest_data['categories'][cat] = manifest_data['categories'].get(cat, 0) + 1
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f, indent=2)
        
        log.info(f"Manifest saved to {manifest_path}")
        return manifest_path
    
    def generate_summary(self) -> str:
        """Generate summary of manifest."""
        total = len(self.entries)
        categories = {}
        
        for entry in self.entries:
            cat = entry.category
            categories[cat] = categories.get(cat, 0) + 1
        
        summary = f"\n[bold]Manifest Summary[/bold]\n"
        summary += f"Total Components: {total}\n\n"
        summary += "[bold]By Category:[/bold]\n"
        
        for cat, count in sorted(categories.items()):
            summary += f"  {cat}: {count}\n"
        
        return summary


# ============================================================================
# Main Application
# ============================================================================

class SDCO:
    """Smart Datasheet Collector & Organizer main application."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = Config(config_path)
        self.llm = LLMClient(self.config)
        self.download_manager = DownloadManager(self.config)
        self.pdf_extractor = PDFMetadataExtractor()
        self.manifest = None
        self.output_dir = None
        self.failed_downloads: List[Tuple[Component, str]] = []
        self.existing_files: List[str] = []
    
    def setup_output_directory(self, base_dir: Optional[str] = None) -> Path:
        """Set up output directory structure."""
        if base_dir is None:
            base_dir = self.config.get('output.base_directory', './datasheets')
        
        self.output_dir = Path(base_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create category subdirectories
        for category in ComponentCategory:
            if category != ComponentCategory.UNKNOWN:
                cat_dir = self.output_dir / category.value
                cat_dir.mkdir(exist_ok=True)
        
        # Collect existing files for duplicate detection
        if self.config.get('advanced.enable_duplicate_detection', True):
            self.existing_files = [
                str(f) for f in self.output_dir.rglob('*.pdf')
            ]
        
        log.info(f"Output directory: {self.output_dir.absolute()}")
        return self.output_dir
    
    async def process_bom(self, bom_file: str, skip_classification: bool = False):
        """Process a BOM file."""
        # Parse BOM
        bom_path = Path(bom_file)
        if not bom_path.exists():
            log.error(f"BOM file not found: {bom_path}")
            return
        
        log.info(f"Parsing BOM: {bom_path}")
        
        if bom_path.suffix.lower() in ['.csv']:
            components = BOMParser.parse_csv(str(bom_path))
        elif bom_path.suffix.lower() in ['.xlsx', '.xls']:
            components = BOMParser.parse_excel(str(bom_path))
        elif bom_path.suffix.lower() in ['.txt']:
            components = BOMParser.parse_text(str(bom_path))
        else:
            log.error(f"Unsupported BOM format: {bom_path.suffix}")
            return
        
        log.info(f"Found {len(components)} components in BOM")
        
        # Setup output
        self.setup_output_directory()
        self.manifest = ManifestGenerator(self.output_dir)
        
        # Process components
        await self.process_components(components, skip_classification)
        
        # Save manifest
        self.manifest.save()
        
        # Log failures
        self.log_failures()
    
    async def process_components(self, components: List[Component], skip_classification: bool = False):
        """Process list of components."""
        # Classification phase
        if not skip_classification:
            log.info("\n[bold blue]Classifying components...[/bold blue]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Classifying...", total=len(components))
                
                for component in components:
                    try:
                        category = await self.llm.classify_component(component)
                        component.category = category
                    except Exception as e:
                        log.debug(f"Classification failed for {component.part_number}: {e}")
                        component.category = self.llm._fallback_classification(component)
                    
                    progress.advance(task)
        
        # Download phase
        log.info("\n[bold blue]Downloading datasheets...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Downloading...", total=len(components))
            
            semaphore = asyncio.Semaphore(self.config.get('download.max_concurrent', 5))
            
            async def download_with_semaphore(component: Component):
                async with semaphore:
                    await self.download_component(component)
                    progress.advance(task)
            
            tasks = [download_with_semaphore(comp) for comp in components]
            await asyncio.gather(*tasks)
    
    async def download_component(self, component: Component):
        """Download datasheet for a single component."""
        # Determine target directory based on category
        if component.category != ComponentCategory.UNKNOWN:
            target_dir = self.output_dir / component.category.value
        else:
            target_dir = self.output_dir / 'Unknown'
            target_dir.mkdir(exist_ok=True)
        
        # Attempt download
        result = await self.download_manager.download_for_component(component, target_dir)
        
        if result.success:
            component.datasheet_url = result.url
            component.datasheet_path = result.file_path
            component.download_status = 'success'
            
            # Calculate hash
            file_hash = self.pdf_extractor.calculate_hash(result.file_path)
            
            # Check for duplicates
            if self.config.get('advanced.enable_duplicate_detection', True):
                if self.pdf_extractor.check_duplicate(result.file_path, self.existing_files):
                    log.warning(f"Duplicate detected: {result.file_path}")
                    # Optionally remove duplicate
                else:
                    self.existing_files.append(result.file_path)
            
            # Extract metadata if enabled
            if self.config.get('advanced.pdf_metadata_extraction', True):
                try:
                    metadata = await self.llm.extract_metadata(result.file_path)
                    component.metadata = metadata
                except Exception as e:
                    log.debug(f"Metadata extraction failed: {e}")
            
            # Add to manifest
            self.manifest.add_entry(component, result.file_path, file_hash)
            
            log.debug(f"✓ Downloaded: {component.part_number} -> {result.file_path}")
        else:
            component.download_status = 'failed'
            component.error_message = result.error
            self.failed_downloads.append((component, result.error))
            log.debug(f"✗ Failed: {component.part_number} - {result.error}")
    
    def log_failures(self):
        """Log failed downloads."""
        if not self.failed_downloads:
            log.info("\n[bold green]All datasheets downloaded successfully![/bold green]")
            return
        
        log.warning(f"\n[bold yellow]{len(self.failed_downloads)} downloads failed[/bold yellow]")
        
        # Save to CSV
        failed_file = self.output_dir / self.config.get('output.failed_file', 'missing_datasheets.csv')
        
        with open(failed_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Part Number', 'Manufacturer', 'Description', 'Error', 'Suggested Search'])
            
            for component, error in self.failed_downloads:
                search_url = f"https://www.google.com/search?q={quote_plus(component.part_number + ' datasheet')}"
                writer.writerow([
                    component.part_number,
                    component.manufacturer,
                    component.description,
                    error,
                    search_url
                ])
        
        log.info(f"Failed downloads logged to: {failed_file}")
        
        # Print summary
        console.print("\n[bold red]Failed Downloads:[/bold red]")
        for component, error in self.failed_downloads[:10]:  # Show first 10
            console.print(f"  • {component.part_number}: {error}")
        
        if len(self.failed_downloads) > 10:
            console.print(f"  ... and {len(self.failed_downloads) - 10} more")


# ============================================================================
# CLI Interface
# ============================================================================

@click.group()
@click.version_option(version='1.0.0', prog_name='SDCO')
def cli():
    """Smart Datasheet Collector & Organizer (SDCO)
    
    Automatically download and organize component datasheets from BOM files.
    """
    pass


@cli.command()
@click.argument('bom_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--config', '-c', type=click.Path(), default='config.yaml', help='Config file')
@click.option('--skip-classification', is_flag=True, help='Skip LLM classification')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def process(bom_file: str, output: str, config: str, skip_classification: bool, verbose: bool):
    """Process a BOM file and download datasheets."""
    if verbose:
        log.setLevel(logging.DEBUG)
    
    sdco = SDCO(config)
    
    console.print("\n[bold blue]🚀 Smart Datasheet Collector & Organizer[/bold blue]\n")
    console.print(f"BOM File: {bom_file}")
    if output:
        console.print(f"Output Directory: {output}")
    console.print()
    
    asyncio.run(sdco.process_bom(bom_file, skip_classification))
    
    # Print summary
    if sdco.manifest:
        console.print(sdco.manifest.generate_summary())


@cli.command()
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--config', '-c', type=click.Path(), default='config.yaml', help='Config file')
def interactive(output: str, config: str):
    """Interactive mode - enter components manually."""
    sdco = SDCO(config)
    
    console.print("\n[bold blue]🚀 Smart Datasheet Collector & Organizer - Interactive Mode[/bold blue]\n")
    
    components = BOMParser.interactive_mode()
    
    if not components:
        console.print("[yellow]No components entered.[/yellow]")
        return
    
    sdco.setup_output_directory(output)
    sdco.manifest = ManifestGenerator(sdco.output_dir)
    
    console.print(f"\nProcessing {len(components)} components...\n")
    asyncio.run(sdco.process_components(components))
    
    sdco.manifest.save()
    sdco.log_failures()
    console.print(sdco.manifest.generate_summary())


@cli.command()
@click.option('--clipboard', is_flag=True, help='Paste from clipboard')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def paste(clipboard: bool, output: str):
    """Process component list from clipboard or stdin."""
    import sys
    
    if clipboard:
        try:
            import pyperclip
            text = pyperclip.paste()
        except ImportError:
            console.print("[red]pyperclip not installed. Install with: pip install pyperclip[/red]")
            return
    else:
        console.print("Paste your component list (Ctrl+D to finish):")
        text = sys.stdin.read()
    
    # Parse pasted text
    lines = text.strip().split('\n')
    components = []
    
    for line in lines:
        if line.strip():
            # Try to parse CSV format
            parts = line.split(',')
            if len(parts) >= 2:
                component = Component(
                    ref=parts[0].strip() if len(parts) > 0 else '',
                    part_number=parts[1].strip() if len(parts) > 1 else '',
                    manufacturer=parts[2].strip() if len(parts) > 2 else '',
                    description=parts[3].strip() if len(parts) > 3 else '',
                    quantity=int(parts[4].strip()) if len(parts) > 4 and parts[4].strip().isdigit() else 1
                )
            else:
                # Just part number
                component = Component(
                    ref='',
                    part_number=line.strip(),
                    manufacturer='',
                    description='',
                    quantity=1
                )
            components.append(component)
    
    if not components:
        console.print("[yellow]No components found in input.[/yellow]")
        return
    
    sdco = SDCO()
    sdco.setup_output_directory(output)
    sdco.manifest = ManifestGenerator(sdco.output_dir)
    
    console.print(f"\nProcessing {len(components)} components...\n")
    asyncio.run(sdco.process_components(components))
    
    sdco.manifest.save()
    sdco.log_failures()


@cli.command()
def version():
    """Show version information."""
    console.print("[bold]SDCO[/bold] v1.0.0")
    console.print("Smart Datasheet Collector & Organizer")


@cli.command()
def init():
    """Initialize configuration files."""
    console.print("\n[bold blue]Initializing SDCO configuration...[/bold blue]\n")
    
    # Copy example config
    import shutil
    config_src = Path(__file__).parent / 'config.yaml'
    config_dst = Path.cwd() / 'config.yaml'
    
    if not config_dst.exists():
        shutil.copy(config_src, config_dst)
        console.print(f"✓ Created config.yaml")
    else:
        console.print("• config.yaml already exists")
    
    # Copy example env
    env_src = Path(__file__).parent / '.env.example'
    env_dst = Path.cwd() / '.env'
    
    if not env_dst.exists():
        shutil.copy(env_src, env_dst)
        console.print(f"✓ Created .env")
    else:
        console.print("• .env already exists")
    
    # Create output directory
    output_dir = Path.cwd() / 'datasheets'
    output_dir.mkdir(exist_ok=True)
    console.print(f"✓ Created datasheets directory")
    
    console.print("\n[green]Initialization complete![/green]")
    console.print("\nNext steps:")
    console.print("  1. Edit config.yaml to customize settings")
    console.print("  2. Set API keys in .env file (optional)")
    console.print("  3. Run: sdco process your_bom.csv")


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
