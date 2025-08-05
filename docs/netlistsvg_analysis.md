# NetlistSVG Skin Definition Analysis

## Overview
This document analyzes the [netlistsvg](https://github.com/nturley/netlistsvg) skin definition format and explores how our ltspice_to_svg project could adapt its output to be compatible with netlistsvg's component library system.

## NetlistSVG's Implementation Strategy

### 1. Template-Based Architecture
The SVG file serves as a **component library** rather than a rendered schematic. Each `<g>` element defines a reusable component template with:
- Component geometry and visual appearance
- Port connection points
- Metadata for layout engines

### 2. Custom Namespace & Semantic Markup
They use the custom namespace:
```xml
xmlns:s="https://github.com/nturley/netlistsvg"
```

**Key Attributes:**
- `s:type` - Component type identifier (e.g., "resistor_h", "capacitor_v")
- `s:width`, `s:height` - Component dimensions for layout calculation
- `s:alias` - Alternative names for component matching
- `s:x`, `s:y`, `s:pid`, `s:position` - Port definitions for connection points

### 3. Styling Strategy: CSS Classes Over Inline Styles
They define global styles in a `<style>` block:

```xml
<style>
.symbol {
  stroke-linejoin: round;
  stroke-linecap: round;
  stroke-width: 2;
}
.connect { /* connection lines */ }
.detail { /* component details */ }
.nodelabel { text-anchor: middle; }
.inputPortLabel { text-anchor: end; }
</style>
```

Then apply classes to elements:
```xml
<path d="M10,0 H40 V10 H10 Z" class="symbol $cell_id"/>
<path d="M0,5 H10 M40,5 H50" class="connect $cell_id"/>
```

**Benefits:**
- Concise markup without repeated inline styles
- Easy global style modifications
- Better human readability
- Smaller file sizes

### 4. Port Definition System
Each component defines precise connection points using invisible `<g>` elements:
```xml
<g s:x="0" s:y="5" s:pid="A" s:position="left"/>
<g s:x="50" s:y="5" s:pid="B" s:position="right"/>
<g s:x="10" s:y="0" s:pid="C" s:position="top"/>
```

**Port Attributes:**
- `s:x`, `s:y` - Absolute coordinates within the component
- `s:pid` - Port identifier (matches netlist connections)
- `s:position` - Port position hint for layout ("left", "right", "top", "bottom")

### 5. Layout Engine Integration
Layout configuration is embedded directly in the SVG:
```xml
<s:layoutEngine
    org.eclipse.elk.layered.spacing.nodeNodeBetweenLayers="20"
    org.eclipse.elk.spacing.nodeNode="35"
    org.eclipse.elk.direction="DOWN"/>
```

### 6. Dynamic Content Support
Text elements use `s:attribute` for runtime substitution:
```xml
<text s:attribute="ref">X1</text>     <!-- Reference designator -->
<text s:attribute="value">10k</text>  <!-- Component value -->
<text s:attribute="name">VCC</text>   <!-- Net/node name -->
```

### 7. Component Categories
Components are organized by type:
- **Power**: vcc, vee, gnd
- **Signal**: inputExt, outputExt
- **Passives**: resistor_h/v, capacitor_h/v, inductor_h/v
- **Sources**: voltage_source, current_source
- **Semiconductors**: diode variants, transistor_npn/pnp
- **Generic**: fallback template with configurable ports

## Adaptation Strategy for ltspice_to_svg

### 1. Port Connection Metadata ✅ **IMPLEMENT**
**Current State**: We parse pin/port information from .asy symbol files but don't embed it in SVG output.

**Required Changes**:
- Add port definitions to symbol rendering
- Extract pin coordinates and identifiers from parsed symbol data
- Generate `<g>` elements with `s:x`, `s:y`, `s:pid`, `s:position` attributes

**Example Implementation**:
```xml
<g s:type="nmos" s:width="64" s:height="128">
  <!-- Symbol geometry -->
  <path d="..." class="symbol"/>
  
  <!-- Port definitions -->
  <g s:x="32" s:y="0" s:pid="D" s:position="top"/>    <!-- Drain -->
  <g s:x="0" s:y="64" s:pid="G" s:position="left"/>   <!-- Gate -->
  <g s:x="32" s:y="128" s:pid="S" s:position="bottom"/> <!-- Source -->
  <g s:x="32" s:y="96" s:pid="B" s:position="right"/>  <!-- Body -->
</g>
```

### 2. CSS Classes Implementation ✅ **IMPLEMENT**
**Benefits**: More concise, readable, and maintainable output.

**Proposed CSS Classes**:
```css
.symbol { stroke: black; stroke-width: 2; stroke-linecap: round; fill: none; }
.wire { stroke: black; stroke-width: 2; stroke-linecap: round; }
.text { fill: black; font-family: Arial; font-size: 12px; }
.flag { fill: red; stroke: red; }
.shape { stroke: black; fill: none; }
```

**Implementation Strategy**:
- Add CSS `<style>` block to SVG header
- Replace inline styles with class attributes
- Use semantic class names aligned with netlistsvg conventions

### 3. Layout Engine Configuration ❌ **SKIP**
**Assessment**: Not relevant for our use case. Layout engines are for automatic netlist-to-schematic conversion.

**Reasoning**: 
- We convert existing LTspice schematics (fixed layouts)
- Manual insertion possible when creating skin files
- Focus resources on ports and styling

### 4. Dynamic Attribute Substitution ✅ **CLARIFY**
**Question**: Should text display literal values when viewed outside netlistsvg runtime?

**Answer**: **YES** - Text should display literal values by default.

**Reasoning**:
- SVG files should be standalone viewable
- Dynamic substitution is runtime behavior for netlistsvg
- Literal values provide meaningful fallback content

**Implementation**:
```xml
<!-- Good: Shows actual component value -->
<text s:attribute="value">10k</text>

<!-- Good: Shows actual reference designator -->
<text s:attribute="ref">R1</text>

<!-- Good: Shows actual net name -->  
<text s:attribute="name">VCC</text>
```

## Implementation Priority

### Phase 1: CSS Classes
1. Define CSS classes for common element types
2. Refactor renderers to use classes instead of inline styles
3. Add `<style>` block to SVG output

### Phase 2: Port Metadata
1. Extract port information from parsed .asy symbols
2. Add port definition generation to symbol renderer
3. Include `s:x`, `s:y`, `s:pid`, `s:position` attributes

### Phase 3: Dynamic Attributes (Optional)
1. Add `s:attribute` support for component values
2. Extract component parameters from .asc files
3. Generate appropriate attribute references

## File Structure Comparison

### Current ltspice_to_svg Output
```xml
<g s:type="nmos" s:width="64" s:height="128" transform="translate(704,336)">
  <line x1="0" y1="64" x2="48" y2="64" 
        stroke="black" stroke-linecap="round" stroke-width="2.0"/>
  <line x1="16" y1="48" x2="16" y2="80" 
        stroke="black" stroke-linecap="round" stroke-width="2.0"/>
  <!-- More repeated inline styles... -->
</g>
```

### Proposed netlistsvg-Compatible Output
```xml
<style>
.symbol { stroke: black; stroke-width: 2; stroke-linecap: round; fill: none; }
.connect { stroke: black; stroke-width: 2; stroke-linecap: round; }
</style>

<g s:type="nmos" s:width="64" s:height="128" transform="translate(704,336)">
  <s:alias val="nmos"/>
  <s:alias val="n_mosfet"/>
  
  <!-- Symbol geometry -->
  <line x1="0" y1="64" x2="48" y2="64" class="connect"/>
  <line x1="16" y1="48" x2="16" y2="80" class="symbol"/>
  
  <!-- Port definitions -->
  <g s:x="32" s:y="0" s:pid="D" s:position="top"/>
  <g s:x="0" s:y="64" s:pid="G" s:position="left"/>
  <g s:x="32" s:y="128" s:pid="S" s:position="bottom"/>
</g>
```

## Benefits of Adaptation

1. **Interoperability**: Generated SVGs could be used as netlistsvg skin components
2. **Conciseness**: CSS classes reduce file size and improve readability
3. **Maintainability**: Global style changes without editing individual elements
4. **Semantic Clarity**: Port metadata enables programmatic analysis
5. **Tool Ecosystem**: Leverage existing netlistsvg tooling and community

## Next Steps

1. Review current symbol parsing code for port information extraction
2. Design CSS class taxonomy for different element types
3. Implement CSS-based styling in renderers
4. Add port metadata generation to symbol renderer
5. Test compatibility with netlistsvg tools 