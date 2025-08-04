# MEOW Format Usage Guide

Complete guide for using the MEOW Image File Format tools.

## Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Launch GUI**: `python meow_gui.py`

## Applications Overview

### 1. Complete GUI (`meow_gui.py`)
A full-featured application with tabs for all operations.

**Features:**
- Convert PNG ↔ MEOW with file browsers
- Image viewer with zoom controls
- File information analyzer
- Status logging
- Menu system

**Usage:**
```bash
python meow_gui.py
```

### 2. Simple Viewer (`meow_viewer.py`)
Lightweight viewer for MEOW files.

**Features:**
- Open and display MEOW images
- Zoom in/out/reset
- Save as PNG
- View metadata and file info
- Scrollable canvas for large images

**Usage:**
```bash
python meow_viewer.py                    # Open file dialog
python meow_viewer.py image.meow         # Open specific file
```

### 3. Command Line Converter (`meow_converter.py`)
Batch conversion and file analysis tool.

**Commands:**
```bash
# Convert PNG to MEOW
python meow_converter.py compile input.png [output.meow]

# Convert MEOW to PNG  
python meow_converter.py extract input.meow [output.png]

# Show file information
python meow_converter.py info file.meow
```

**Examples:**
```bash
python meow_converter.py compile photo.png
python meow_converter.py extract photo.meow converted.png
python meow_converter.py info photo.meow
```

### 4. Core Library (`meow_format.py`)
The underlying implementation for custom applications.

**Basic Usage:**
```python
from meow_format import MeowFormat

# Initialize
meow = MeowFormat()

# Convert PNG to MEOW
success = meow.png_to_meow("input.png", "output.meow")

# Load MEOW as PIL Image
image = meow.meow_to_image("file.meow")

# Get file information
info = meow.get_file_info("file.meow")

# Access metadata
print(meow.metadata)
```

## File Format Details

### Header Structure
```
Offset  Size  Description
------  ----  -----------
0x00    4     Magic number "MEOW" (ASCII)
0x04    4     Width (uint32, little endian)
0x08    4     Height (uint32, little endian)
```

### Pixel Data
- **Format**: RGBA (Red, Green, Blue, Alpha)
- **Size**: 4 bytes per pixel
- **Order**: Row-major (left-to-right, top-to-bottom)
- **Range**: 0-255 per channel

### Metadata (Optional)
- **Format**: Key-value pairs
- **Encoding**: UTF-8 strings
- **Structure**: [key_length][key][value_length][value]...

## Advanced Usage

### Batch Processing
Convert multiple files using Python:

```python
from meow_format import MeowFormat
import glob

meow = MeowFormat()

# Convert all PNGs in a directory
for png_file in glob.glob("*.png"):
    meow_file = png_file.replace(".png", ".meow")
    if meow.png_to_meow(png_file, meow_file):
        print(f"Converted: {png_file} -> {meow_file}")
```

### Custom Metadata
Add custom metadata to MEOW files:

```python
from meow_format import MeowFormat

meow = MeowFormat()

# Add custom metadata before conversion
meow.metadata["author"] = "Your Name"
meow.metadata["description"] = "My awesome image"
meow.metadata["camera"] = "Canon EOS R5"

meow.png_to_meow("photo.png", "photo.meow")
```

### File Validation
Check if a file is a valid MEOW file:

```python
from meow_format import MeowFormat

meow = MeowFormat()
info = meow.get_file_info("suspicious.meow")

if info and info['format'] == 'MEOW':
    print("Valid MEOW file")
    print(f"Dimensions: {info['width']}x{info['height']}")
else:
    print("Not a valid MEOW file")
```

## Integration Examples

### Web Application
```python
from flask import Flask, request, send_file
from meow_format import MeowFormat
from PIL import Image
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_to_meow():
    file = request.files['image']
    
    # Save uploaded file
    png_path = f"temp_{file.filename}"
    file.save(png_path)
    
    # Convert to MEOW
    meow = MeowFormat()
    meow_path = png_path.replace('.png', '.meow')
    
    if meow.png_to_meow(png_path, meow_path):
        return send_file(meow_path, as_attachment=True)
    else:
        return "Conversion failed", 400
```

### Desktop Application
```python
import tkinter as tk
from tkinter import filedialog, messagebox
from meow_format import MeowFormat

class SimpleConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.meow = MeowFormat()
        
        tk.Button(self.root, text="Convert PNG to MEOW", 
                 command=self.convert).pack(pady=10)
    
    def convert(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png")]
        )
        
        if file_path:
            meow_path = file_path.replace('.png', '.meow')
            if self.meow.png_to_meow(file_path, meow_path):
                messagebox.showinfo("Success", f"Saved as {meow_path}")
```

## Performance Tips

### Memory Optimization
For large images, consider processing in chunks:

```python
# For very large images, you might want to process tiles
# This is a conceptual example - the current implementation 
# loads the entire image into memory

def process_large_image(png_path, chunk_size=1024):
    # This would require modifications to the core format
    # to support streaming/chunked processing
    pass
```

### Speed Optimization
- Use binary I/O operations directly for maximum speed
- Minimize metadata when file size is critical
- Consider adding compression for production use

## Troubleshooting

### Common Issues

**Import Error**: Module not found
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Memory Error**: Large images
```bash
# Solution: Reduce image size or add swap space
# The format stores uncompressed RGBA data
```

**Permission Error**: Cannot write file
```bash
# Solution: Check file permissions and disk space
```

**Invalid MEOW File**: Corruption or wrong format
```python
# Solution: Validate file before processing
info = meow.get_file_info("file.meow")
if not info:
    print("File is not a valid MEOW format")
```

### Debugging

Enable detailed error reporting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your MEOW operations here
```

### Platform-Specific Notes

**Windows**: 
- Use batch file launcher for easy access
- File associations work with admin privileges

**Linux/macOS**: 
- May need to install tkinter separately
- Use `python3` instead of `python` if needed

## Contributing

The MEOW format is designed to be simple and extensible. 

**Potential enhancements:**
- Compression algorithms (LZ4, zlib)
- Multiple color spaces (sRGB, Adobe RGB)
- Animation support (frame sequences)
- Layer support (Photoshop-style)
- HDR support (floating-point channels)

**Code structure:**
- `meow_format.py`: Core format implementation
- `meow_format.py`: Core MEOW format implementation
- `meow_gui.py`: Complete GUI application with AI detection
