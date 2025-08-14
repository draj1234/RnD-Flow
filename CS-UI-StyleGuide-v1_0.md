# ClearSight UI Style Guide
**Version:** v1.0  
**Date:** 2025-08-10  
**Purpose:** Provide a consistent, AI-friendly design and UX framework for all ClearSight web application interfaces.

---

## 1. Color Palette
**Primary Brand Colors:**
- Primary Blue: `#1E88E5` (main accents, buttons, active links)
- Secondary Gray: `#ECEFF1` (background panels, form areas)
- Neutral White: `#FFFFFF` (primary background)

**Functional Status Colors:**
- Success/Completed: `#43A047` (stage passed, ready for next)
- Warning/Pending: `#FB8C00` (requires attention)
- Error/Failed: `#E53935` (failed QC, action required)
- Info: `#29B6F6` (system messages)

**Usage:**  
Always ensure 4.5:1 contrast ratio for text on background per WCAG AA.

---

## 2. Typography
**Fonts:**
- Headings: `Roboto`, sans-serif
- Body Text: `Open Sans`, sans-serif
- Code/Logs: `Source Code Pro`, monospace

**Sizes:**
- H1: 28px bold
- H2: 22px semi-bold
- H3: 18px semi-bold
- Body: 14px regular
- Small/Labels: 12px regular

---

## 3. Layout Principles
- **Grid System:** 12-column responsive grid (Bootstrap or CSS Grid)
- **Spacing:** 8px base unit (margins/padding in multiples of 8)
- **Alignment:** Left-align text; center-align key action buttons
- **Consistency:** Same spacing between related UI elements across pages

---

## 4. Component Standards
**Buttons:**
- Primary: Filled with primary blue, white text
- Secondary: Outlined, blue border, blue text
- Disabled: Light gray fill, gray text

**Tables:**
- Zebra striping for row distinction
- Sortable column headers with icon indicators
- Hover highlight

**Forms:**
- Labels above inputs
- Mandatory fields marked with `*`
- Inline validation messages in red for errors

**Status Badges:**
- Rounded, color-coded based on status colors
- Include icon + text

---

## 5. Responsive Behavior
- **Desktop:** Full layout with side navigation
- **Tablet:** Collapsible navigation, stacked content sections
- **Mobile:** Single-column layout, larger touch targets

---

## 6. Accessibility Guidelines
- All interactive elements must be keyboard navigable
- Provide `aria-label` attributes for icons
- Ensure tooltips for abbreviations or technical terms

---

**Reference:**  
All components will be built in React using Material-UI v5 (MUI) to enforce consistent design implementation.
