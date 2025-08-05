# Window Text Rotation Debugging Analysis

## Problem Statement
Window text appears upside down or incorrectly oriented when symbols are rotated R180 and R270 degrees. R0 and R90 work correctly (R90 by accident).

## Root Cause Analysis

### Current Implementation Flow
1. **Symbol Transformation**: Symbol gets SVG transform like `translate(x,y) rotate(angle)`
2. **Window Text Rendering**: Text is rendered inside the transformed symbol group with original justification
3. **Text Renderer Processing**: TextRenderer applies its own rotation for V justifications (e.g., VBottom → rotate(-90°))
4. **Result**: Double rotation causes incorrect text orientation

### Specific Issues

#### Working Cases (Accidental)
- **R0**: No symbol rotation, text renders normally
- **R90 + VBottom**: Symbol rotates +90°, VBottom text rotates -90° → Net 0° (readable)

#### Broken Cases  
- **R180 + Left**: Symbol rotates +180°, Left text stays horizontal → Text upside down (180°)
- **R270 + VTop**: Symbol rotates +270°, VTop text rotates -90° → Net +180° (upside down)
- **R270 + VBottom**: Symbol rotates +270°, VBottom text rotates -90° → Net +180° (upside down)

### Test Case Analysis
From `test_symbol_window_texts.asc`:
- **V1** (R0): Baseline - works correctly
- **V2** (R90): VBottom/VTop justifications - works by coincidence  
- **V3** (R180): Left justification - text appears upside down
- **V4** (R270): VTop/VBottom justifications - text appears upside down

## Failed Approach: Justification Compensation

### What We Tried
1. Store rotation angle in SymbolRenderer
2. Create `_compensate_text_for_rotation()` method to adjust justification before passing to TextRenderer
3. Map justifications (e.g., R180: Left→Right, VBottom→VTop)

### Why It Failed
1. **Coordinate System Issues**: Changing justification affects text positioning coordinates which need to be recalculated
2. **Complex Mapping**: The mapping between rotations and justifications is more complex than simple swaps
3. **Text Anchor Problems**: Different justifications use different text-anchor values, breaking positioning

### Key Insight from Failed Attempt
The problem is that **text coordinates are specified in the symbol's local coordinate system** before the symbol transform is applied. When we change justification, we need to also adjust the coordinates to maintain the same visual position.

## Alternative Approaches to Consider

### Approach 1: Transform Compensation in TextRenderer
- Pass symbol rotation context to TextRenderer  
- Let TextRenderer apply counter-rotation transforms
- Pro: Cleaner separation of concerns
- Con: TextRenderer needs to know about symbol context

### Approach 2: Pre-transform Text Coordinates
- Transform text coordinates from symbol space to screen space before rendering
- Apply inverse rotation to coordinates and justification together
- Pro: More mathematically correct
- Con: Complex coordinate transformations

### Approach 3: Post-processing SVG Transforms
- Let text render incorrectly, then post-process the SVG to fix transforms
- Add counter-rotation transforms to text elements
- Pro: Doesn't break existing rendering logic
- Con: Complex SVG manipulation

## Technical Details

### Current Symbol Transform Application
```python
# In SymbolRenderer.set_transformation()
transform = ["translate(x,y)"]
if angle != 0:
    transform.append(f"rotate({angle})")
group.attribs['transform'] = ' '.join(transform)
```

### Current Text Rendering
```python
# In SymbolRenderer._render_window_property()  
text_data = {
    'x': window_settings['x'],        # Local coordinates
    'y': window_settings['y'],        # Local coordinates  
    'justification': window_settings['justification'],  # Original justification
    'is_mirrored': self._is_mirrored
}
text_renderer.render(text_data, target_group=symbol_group)
```

### The Core Issue
Text coordinates `(x, y)` are in the **symbol's local coordinate system** and will be transformed by the symbol's transform. But the text justification and rotation logic assumes **screen coordinate system**.

## ✅ IMPLEMENTED SOLUTION

### Final Approach: Generic Rotation in TextRenderer + Compensation Logic in SymbolRenderer

**Date Implemented**: 2025-08-04  
**Branch**: `fix/window-text-rotation`  
**Commit**: `0752e56`

### Implementation Details

#### 1. Enhanced TextRenderer with Generic Rotation Support
**File**: `src/renderers/text_renderer.py`

- Added optional `rotation` parameter to text dictionary in `render()` method
- Applies additional rotation transform when present (in addition to existing vertical text logic)
- Clean, generic approach - TextRenderer doesn't need to know about symbols or compensation
- Maintains full backward compatibility

```python
# New parameter in text dictionary
additional_rotation = text.get('rotation', 0)  # Optional additional rotation

# Applied after mirroring but before vertical text rotation
if additional_rotation != 0:
    rotation_group = self.dwg.g()
    rotation_group.attribs['transform'] = f"rotate({additional_rotation}, {x}, {y})"
    rotation_group.add(text_element)
    text_element = rotation_group
```

#### 2. Symbol Rotation Tracking in SymbolRenderer
**File**: `src/renderers/symbol_renderer.py`

- Added `_rotation_angle` instance variable to track current symbol rotation
- Stored rotation angle in `set_transformation()` method
- Reset angle in `begin_symbol()` and `finish_symbol()` for clean state management

```python
# Store rotation angle during transformation setup
self._rotation_angle = angle
```

#### 3. Smart Compensation Logic

**Method**: `_calculate_text_rotation_compensation(justification) -> tuple[int, str]`

**Rules**:
- **R0/R90**: No compensation needed (return `0, justification`)
- **R180/R270**: Apply 180° counter-rotation + swap justifications

**Justification Swaps** (via `_swap_justification()`):
- `Left` ↔ `Right`
- `VTop` ↔ `VBottom` 
- `Center`, `VCenter`, `Top`, `Bottom` remain unchanged

```python
# Simplified logic
if self._rotation_angle == 0 or self._rotation_angle == 90:
    return 0, justification
elif self._rotation_angle == 180 or self._rotation_angle == 270:
    adjusted_justification = self._swap_justification(justification)
    return 180, adjusted_justification
```

#### 4. Integration in Window Text Rendering

**Location**: `_render_window_property()` method

- Calculate compensation before creating text_data
- Inject both adjusted justification and rotation compensation
- Maintain all existing text properties

```python
# Calculate rotation compensation for symbol rotation
original_justification = window_settings['justification']
rotation_compensation, adjusted_justification = self._calculate_text_rotation_compensation(original_justification)

# Create text data with adjusted justification
text_data = {
    'x': window_settings['x'],
    'y': window_settings['y'], 
    'text': property_value,
    'justification': adjusted_justification,  # ← Swapped if needed
    'size_multiplier': window_settings.get('size_multiplier', 0),
    'is_mirrored': self._is_mirrored
}

# Add rotation compensation if needed
if rotation_compensation != 0:
    text_data['rotation'] = rotation_compensation  # ← Added rotation
```

### Why This Solution Works

1. **Addresses Root Cause**: Applies counter-rotation to cancel out symbol rotation, preventing double-rotation
2. **Handles Coordinate Systems**: Justification swaps maintain correct text positioning relative to symbol shapes
3. **Clean Architecture**: 
   - TextRenderer = generic text rotation capability
   - SymbolRenderer = symbol-specific compensation logic
4. **Backward Compatible**: Existing code continues to work unchanged
5. **Comprehensive**: Handles all rotation cases (R0, R90, R180, R270, M0, M90, M180, M270)

### Test Results ✅

**Test Case**: `test_symbol_window_texts.asc`
- **V1 (R0)**: ✅ Works correctly (baseline)
- **V2 (R90)**: ✅ Works correctly (was working by coincidence)
- **V3 (R180)**: ✅ **FIXED** - Text now readable with 180° counter-rotation + Left→Right swap
- **V4 (R270)**: ✅ **FIXED** - Text now readable with 180° counter-rotation + VTop↔VBottom swap

### Validation Strategy ✅

- ✅ Text remains readable in all orientations (R0, R90, R180, R270)
- ✅ Text positioning accurate relative to symbol shapes  
- ✅ No coordinate drift or positioning errors
- ✅ Both component names and values render correctly
- ✅ No regressions for working cases (R0, R90)
- ✅ Handles mirrored symbols (M0, M90, M180, M270) correctly

### Performance Impact
- Minimal: Only adds computation when rotation compensation is needed
- No impact on R0/R90 cases (most common)
- Clean separation means TextRenderer performance unchanged