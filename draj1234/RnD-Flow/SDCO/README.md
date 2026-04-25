# Smart Datasheet Collector & Organizer (SDCO)

A Python-based CLI tool that automatically searches and downloads datasheets for electronic components from a BOM (Bill of Materials), classifies them using LLM (Local or API), and organizes them into a structured folder hierarchy.

## Features

✅ **Multi-format BOM Input**
- CSV/Excel BOM files
- Plain text lists (one part per line)
- Interactive mode (manual entry)
- Clipboard paste support

✅ **Intelligent Classification**
- LLM-powered categorization (Ollama local or OpenRouter API)
- 12 predefined categories (Power, MCU, Sensors, etc.)
- Fallback keyword-based classification

✅ **Smart Download**
- Multiple source fallback (Manufacturer, Digi-Key, Mouser, Google, etc.)
- Parallel concurrent downloads
- Retry logic with exponential backoff
- Duplicate detection

✅ **Organization**
- Automatic folder structure by category
- Smart file naming convention
- Manifest generation (JSON)
- Failed download tracking

✅ **Metadata Extraction**
- PDF text extraction
- LLM-powered metadata parsing
- SHA256 hash for deduplication

## Installation

### Prerequisites

- Python 3.9+
- pip package manager
- Optional: Ollama (for local LLM) or OpenRouter API key

### Quick Install

```bash
# Clone or navigate to the SDCO directory
cd sdco

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize configuration
python datasheet_collector.py init
```

### Optional: Install Ollama (for local LLM)

**macOS:**
```bash
brew install ollama
ollama pull llama3.1:8b
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
```

**Windows:**
Download from [https://ollama.com/download](https://ollama.com/download)

Then run:
```bash
ollama pull llama3.1:8b
```

## Configuration

### Basic Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `config.yaml` to customize:
- LLM provider (ollama or openrouter)
- Download settings (concurrency, timeouts)
- Output directory
- Category mappings

3. Set API keys in `.env` (optional):
```bash
OPENROUTER_API_KEY=your_key_here
DIGIKEY_CLIENT_ID=your_client_id
DIGIKEY_CLIENT_SECRET=your_secret
MOUSER_API_KEY=your_api_key
```

### Configuration Options

See `config.yaml` for all available options:

```yaml
llm:
  provider: "ollama"  # or "openrouter"
  model: "llama3.1:8b"
  timeout: 120
  
download:
  max_concurrent: 5
  timeout: 30
  retries: 3
  
output:
  base_directory: "./datasheets"
  manifest_file: "manifest.json"
```

## Usage

### Process a BOM File

```bash
# Basic usage
python datasheet_collector.py process example_bom_echotag_v2.csv

# With custom output directory
python datasheet_collector.py process bom.csv -o ./my_datasheets

# Skip LLM classification (use keyword-only)
python datasheet_collector.py process bom.csv --skip-classification

# Verbose output
python datasheet_collector.py process bom.csv -v
```

### Interactive Mode

```bash
python datasheet_collector.py interactive
```

Enter components one by one when prompted.

### Paste from Clipboard

```bash
# From clipboard (requires pyperclip)
pip install pyperclip
python datasheet_collector.py paste --clipboard

# From stdin
python datasheet_collector.py paste
# Then paste your list and press Ctrl+D (Unix) or Ctrl+Z (Windows)
```

### Initialize Configuration

```bash
python datasheet_collector.py init
```

Creates default config files and directories.

## Output Structure

After processing, datasheets are organized as follows:

```
datasheets/
├── Power/
│   ├── MCP1700T-3302E_TT_Microchip_Technology.pdf
│   └── TPS62740DSSR_Texas_Instruments.pdf
├── MCU_Processor/
│   └── NRF52840-DT-R_Nordic_Semiconductor.pdf
├── Memory/
│   └── AT25SF128A-SSHN-B_Adesto_Technologies.pdf
├── Sensors/
│   └── LIS2DH12TR_STMicroelectronics.pdf
├── Passives/
│   ├── GRM155R61A105KA12D_Murata.pdf
│   └── RC0402FR-0710KL_Yageo.pdf
├── Connectors/
│   └── 52492-0101_Molex.pdf
├── Protection/
│   └── USBLC6-2SC6_STMicroelectronics.pdf
├── Clock_Timing/
│   └── TCXO-32.768KHZ-ECS-2050_ECS_Inc.pdf
├── Wireless_Comms/
│   └── ...
├── manifest.json
└── missing_datasheets.csv
```

### Manifest File

The `manifest.json` contains:

```json
{
  "generated_at": "2024-01-15T10:30:00",
  "total_components": 30,
  "categories": {
    "Power": 5,
    "MCU_Processor": 2,
    "Sensors": 3,
    ...
  },
  "entries": [
    {
      "part_number": "NRF52840-DT-R",
      "manufacturer": "Nordic Semiconductor",
      "category": "Wireless_Comms",
      "datasheet_file": "Wireless_Comms/NRF52840-DT-R_Nordic_Semiconductor.pdf",
      "file_hash": "abc123...",
      "metadata": {...}
    }
  ]
}
```

### Failed Downloads

Failed downloads are logged to `missing_datasheets.csv` with:
- Part number
- Manufacturer
- Error message
- Suggested Google search URL

## Component Categories

SDCO classifies components into these categories:

| Category | Description | Examples |
|----------|-------------|----------|
| Power | Voltage regulators, PMICs, chargers | LDOs, DC-DC converters |
| MCU_Processor | Microcontrollers, processors | nRF52, STM32, ESP32 |
| Memory | Flash, EEPROM, RAM | AT25SF, CAT24C |
| Sensors | Accelerometers, temperature, etc. | LIS2DH, BME280 |
| Wireless_Comms | BLE, WiFi, LoRa, UWB | nRF modules, ESP |
| Passives | Resistors, capacitors, inductors | 0402, 0602 components |
| Connectors | USB, headers, jacks | USB-C, pin headers |
| Protection | ESD, fuses, TVS diodes | USBLC6, resettable fuses |
| Clock_Timing | Crystals, oscillators | 32.768kHz, TCXO |
| Interface | Level shifters, transceivers | SN74LVC, isolators |
| Mechanical | Enclosures, mounting hardware | Cases, standoffs |
| Reference_Docs | Application notes, guides | AN documents |

## Advanced Features

### Duplicate Detection

SDCO automatically detects duplicate files using SHA256 hashing. Enable/disable in `config.yaml`:

```yaml
advanced:
  enable_duplicate_detection: true
```

### Metadata Extraction

Extract component metadata from PDF datasheets:

```yaml
advanced:
  pdf_metadata_extraction: true
```

### Custom Categories

Add or modify categories in `config.yaml`:

```yaml
categories:
  - name: "Custom_Category"
    keywords: ["keyword1", "keyword2"]
```

## Troubleshooting

### Ollama Not Found

If you get "Ollama not found" error:
1. Install Ollama from [ollama.com](https://ollama.com)
2. Pull a model: `ollama pull llama3.1:8b`
3. Or use OpenRouter API instead (set `OPENROUTER_API_KEY`)

### Download Failures

Common causes:
- Website blocking automated requests (try different user-agent in config)
- Part number format issues (check manufacturer website)
- Discontinued components

Check `missing_datasheets.csv` for failed downloads with suggested search URLs.

### Slow Performance

Adjust concurrent downloads in `config.yaml`:

```yaml
download:
  max_concurrent: 10  # Increase for faster downloads
```

### Memory Issues

For large BOMs (>100 components), consider:
- Reducing `max_concurrent`
- Processing in batches
- Increasing system memory

## Example: Echotag V2 BOM

Process the included example BOM:

```bash
python datasheet_collector.py process example_bom_echotag_v2.csv -v
```

This will process 30 components from the Echotag V2 design, including:
- nRF52840 UWB/BLE module
- AT25SF128A flash memory
- LIS2DH12 accelerometer
- Various passives and connectors

Expected output: ~25-28 successful downloads (some generic parts may not have datasheets).

## Development

### Project Structure

```
sdco/
├── datasheet_collector.py  # Main application
├── config.yaml             # Configuration
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── example_bom_echotag_v2.csv
└── README.md              # This file
```

### Adding New Sources

To add a new datasheet source:

```python
class NewSource(DatasheetSource):
    async def search(self, part_number: str, manufacturer: str) -> List[str]:
        # Implement search logic
        return [url1, url2]
    
    async def download(self, url: str, save_path: str) -> DownloadResult:
        # Implement download logic
        return result
```

Then add to `DownloadManager.sources` list.

## Contributing

Contributions welcome! Areas for improvement:
- Additional distributor APIs (Digi-Key, Mouser official APIs)
- Web interface (Flask/FastAPI)
- Browser extension
- Better PDF parsing
- More manufacturer website support

## License

MIT License - See LICENSE file for details.

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in `download_log.txt`
3. Ensure Ollama is running (if using local LLM)
4. Verify API keys are set correctly

---

**Built with ❤️ for electronics engineers and hobbyists**
