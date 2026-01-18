# Python 3 Migration Plan for OrangePi GPIO Library

## Overview
This document outlines the plan to convert Python 2 code to Python 3 for the OrangePi GPIO library. The library is based on pyA20 0.2.1 and needs updates to work with Python 3 on Armbian 26.2.0 Trixie (Debian), which has deprecated Python 2.

## Files Requiring Updates

### 1. **setup.py** (Minor changes)
   - **Issue**: Uses `raw_input()` compatibility shim (already has try/except)
   - **Issue**: File reading may need encoding specification for Python 3
   - **Changes Required**:
     - Line 104: `open('README.txt')` should specify encoding: `open('README.txt', encoding='utf-8')`
     - Line 104: Same for `CHANGES.txt`
     - Already has Python 3 compatibility for `raw_input()`

### 2. **pyA20/utilities/color.py** (Major changes)
   - **Issues**: Uses Python 2 `print` statements without parentheses throughout
   - **Changes Required**:
     - Lines 9-73: Convert all `print` statements to `print()` function calls
     - All print statements in the `test()` method need parentheses
     - Total: ~34 print statements to convert

### 3. **examples/blink_led.py** (Minor changes)
   - **Issue**: Shebang uses `python` instead of `python3`
   - **Changes Required**:
     - Line 1: Change `#!/usr/bin/env python` to `#!/usr/bin/env python3`
     - Already uses `print()` with parentheses (correct)

### 4. **examples/blink_led_PG6.py** (Moderate changes)
   - **Issues**: 
     - Shebang uses `python` instead of `python3`
     - Uses Python 2 `print` statements without parentheses
     - Inconsistent indentation (lines 36, 39, 41-47)
   - **Changes Required**:
     - Line 1: Change shebang to `python3`
     - Lines 36, 39: Convert `print "led set 1 \r\n"` and `print "led set 0 \r\n"` to `print("led set 1 \r\n")`
     - Fix indentation issues (mixed tabs/spaces)

### 5. **examples/blink_POWER_STATUS_PL10.py** (Moderate changes)
   - **Issues**: 
     - Shebang uses `python` instead of `python3`
     - Uses Python 2 `print` statements without parentheses
     - Inconsistent indentation (lines 48, 51, 53-59)
   - **Changes Required**:
     - Line 1: Change shebang to `python3`
     - Lines 48, 51: Convert `print "led set 1 \r\n"` and `print "led set 0 \r\n"` to `print("led set 1 \r\n")`
     - Fix indentation issues (mixed tabs/spaces)

### 6. **examples/read_button.py** (Minor changes)
   - **Issue**: Shebang uses `python` instead of `python3`
   - **Changes Required**:
     - Line 1: Change `#!/usr/bin/env python` to `#!/usr/bin/env python3`
     - Already uses `print()` with parentheses (correct)

### 7. **examples/read_eeprom.py** (Major changes)
   - **Issues**: 
     - Shebang uses `python` instead of `python3`
     - Uses Python 2 `print` statements without parentheses
     - Uses `xrange()` which doesn't exist in Python 3 (should be `range()`)
     - May have bytes vs string issues with `i2c.read()` return values
     - Comment on line 7 mentions Python 3 incompatibility
   - **Changes Required**:
     - Line 1: Change shebang to `python3`
     - Lines 29-39: Convert all `print` statements to `print()` function calls
     - Lines 33, 37: Replace `xrange(16)` with `range(16)`
     - Line 42: Replace `xrange(128)` with `range(128)`
     - Line 45: Replace `xrange(0, 16)` with `range(0, 16)` or `range(16)`
     - Line 50: Replace `xrange(16)` with `range(16)`
     - Lines 43-55: Verify `i2c.read()` returns bytes or list, handle accordingly
     - Line 52: `chr(page[j])` - ensure `page[j]` is integer, not byte

### 8. **examples/read_key_PG7.py** (Moderate changes)
   - **Issues**: 
     - Shebang uses `python` instead of `python3`
     - Uses Python 2 `print` statements without parentheses
     - Uses old-style string formatting with `print` (line 46, 51)
     - Inconsistent indentation (lines 44-54)
   - **Changes Required**:
     - Line 1: Change shebang to `python3`
     - Line 46: Convert `print "led out value is %d"%value_out` to `print("led out value is %d" % value_out)`
     - Line 51: Convert `print "get button state is %d"%state` to `print("get button state is %d" % state)`
     - Fix indentation issues (mixed tabs/spaces)

### 9. **Other __init__.py files** (No changes)
   - `pyA20/__init__.py` - Simple author declaration, no changes needed
   - `pyA20/gpio/__init__.py` - Simple author declaration, no changes needed
   - `pyA20/gpio/connector/__init__.py` - Template file with no executable code
   - `pyA20/gpio/port/__init__.py` - Template file with no executable code
   - `pyA20/i2c/__init__.py` - Simple author declaration, no changes needed
   - `pyA20/spi/__init__.py` - Simple author declaration, no changes needed

## Summary of Changes

### Change Types:
1. **Shebang updates**: 6 files need `python` → `python3`
2. **Print statements**: 4 files need print statement → print() function conversion
3. **xrange()**: 1 file needs `xrange()` → `range()` conversion
4. **File encoding**: 1 file (setup.py) should specify UTF-8 encoding when opening files
5. **Indentation fixes**: 3 files have mixed tabs/spaces that should be standardized to spaces

### Files by Priority:
- **High Priority** (Core functionality): `setup.py`, `examples/read_eeprom.py`, `pyA20/utilities/color.py`
- **Medium Priority** (Example scripts): All example files
- **Low Priority** (Template files): `__init__.py` template files (may be left as-is)

## Testing Recommendations

After migration, test each example script:
1. Verify GPIO initialization works
2. Test LED blinking examples
3. Test button/input reading
4. Test EEPROM reading (verify bytes handling)
5. Ensure all scripts run with `python3` command

## Notes

- The C extension modules (`.c` files) should compile without changes as they use Python C API
- The `distutils` module is deprecated in Python 3.12+ but should still work in Python 3.11
- Consider adding `python_requires='>=3.6'` to setup.py if maintaining backward compatibility is not needed
- The comment in `read_eeprom.py` line 7 mentions "The text will be big mess if python3 is used" - this should be addressed with proper bytes/string handling
