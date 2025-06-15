<h1 align="center">MEOW</h1>

<p align="center">
    <img src="assets/logos/logo.png" alt="MEOW Logo" width="200"/>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Version-1.2-black?color=black&labelColor=black" alt="Version 1.2">
    <img src="https://img.shields.io/badge/License-Apache 2.0-black?color=black&labelColor=black" alt="License Apache 2.0">
    <img src="https://img.shields.io/badge/Platform-Cross--platform-black?color=black&labelColor=black" alt="Platform Cross-platform">
</p>

<p align="center">
     The most Purr-fect Image File Format for your AI workflows
</p>

---

## Wait- What? You Can Just Make File Formats?

<table>
<tr>
<td width="70%">

Well- yes, but no, I'll come to that bit later, but before that, let me geek out about what this project is

**MEOW** (Metadata Encoded Optimized Webfile) is a Python-based image file format designed to be efficient, practical, and cross-platform compatible. 

With support for RGBA transparency, metadata, and fast rendering capabilities, MEOW provides a modern alternative for image storage and manipulation.

Whether you're a developer looking for a lightweight image format, an AI locked-in person to use the best possible file fomat, a digital artist needing transparent image support, or just a curious coder who wants a .meow file extension, MEOW offers a simple yet powerful solution.

</td>
<td width="30%" align="center">

<img src="assets/sample-images/test.png" alt="Sample MEOW Image" width="200"/>
<br>
<em>The First image to ever be converted to .meow</em>
<br>
<sub>Note: GitHub doesn't support .meow files (YET), so had to display the original PNG source</sub>

</td>
</tr>
</table>

## Why is it called MEOW?

<p align="center">
    <img src="assets/readme/meow-name.png" alt="MEOW naming conversation" width="600"/>
</p>

---

## The Problem with "Innovative" File Formats

**MEOW** started off as just a fun, new (very ineffecient) image file format I made studying about them as a meme while having better metadata to be used with AI, but I realised something.

People don't make new file formats simply because of one problem- they're very hard to bring to mass adoption, what if we fix that?

## Cross-Compatibility With PNGs

MEOW uses a steganographic image format that embeds metadata that's needed for AI workflows while maintaining PNG compatibility. It's basically PNGs on Steroids.

<table>
<tr>
<td width="60%">

### How it's less of a headache
Unlike traditional formats that require special viewers, **MEOW files contain standard PNG data**:

- ✅ **Works in ANY image viewer** after simple setup (2 options below)
- ✅ **Option 1: Rename to `.png`** - instant compatibility everywhere
- ✅ **Option 2: File association setup** - makes `.meow` extension recognized  
- ✅ **Hidden AI data** invisible to standard viewers, visible to AI
- ✅ **Cross-platform compatibility** (Windows, macOS, Linux)

**Setup Required**: Either rename `.meow` → `.png` OR run file association scripts

</td>
<td width="40%" align="center">

```
📱 Standard Viewer (Setup Required)
   ↓ Method 1: Rename test.meow → test.png
   ↓ Method 2: Run file association script
🖼️ Result: Opens as beautiful PNG image

🤖 AI-Aware App  
   ↓ Opens .meow file directly (or renamed .png)
🧠 Sees: Image + Rich AI metadata
```

</td>
</tr>
</table>

### Perfect for AI Applications

MEOW is specifically designed for use with AI, embedding metadata that is really useful for machine learning workflows and potentially can enhance LLM image understanding

<table>
<tr>
<td width="50%">

#### Problems with Current Formats
- **Metadata can very easily be stripped** - when images are processed or shared - this is usually for security but is a bad tradeoff for AI
- **Limited to basic descriptive information** - not optimized for machine learning
- **Separate from actual image processing** - requires additional steps
- **Not designed for machine learning workflows**

</td>
<td width="50%">

#### Performance Benefits
- **Reduced preprocessing time** with embedded parameters
- **Training data enrichment** with embedded annotations and other data
- **Enhanced LLM understanding** with structured metadata and features like attention maps
- **Multimodal AI acceleration** for vision-language models, no need for seperate JSONs now

</td>
</tr>
</table>

## MEOW's AI-Optimized Advantages

MEOW embeds AI-specific parameters that traditional formats can't (or well, can with a ton of modification can) handle. When any image is converted to a .meow, this data is automatically added in the conversion process:

1. **Pre-computed AI Features**
  *   Optimal preprocessing parameters embedded in the file
  *   Attention maps showing where AI models should focus
  *   Bounding boxes and object detection data
  *   Saliency regions for computer vision tasks

2.  **Model Optimization Data**

3.  **Steganographic Storage**

  Unlike traditional metadata that's easily lost:

  *   Encoded in pixel LSBs (Least Significant Bits)
  *   Survives file operations that would strip normal metadata
  *   Invisible to standard viewers but accessible to AI applications

## How Steganographic Storage Works

MEOW uses **LSB (Least Significant Bit) steganography** to hide AI data inside standard PNG images:

<table>
<tr>
<td width="60%">

### The Technical Magic
1. **Load standard PNG image** into memory
2. **Compress AI metadata** using compression
3. **Hide data in pixel LSBs** (2 bits per RGB channel = 6 bits/pixel)
4. **Save as PNG** with `.meow` extension
5. **Result**: Perfect PNG that works everywhere + hidden AI data

### Storage Specifications
- **The Magic Header**: `MEOW_STEG_V2` (12 bytes)
- **Capacity**: 6 bits per pixel (RGB channels only)
- **Compression**: zlib level 9 for maximum efficiency
- **Overhead**: Typically 15-25% of original file size

</td>
<td width="40%">

```
Original Pixel: [R, G, B, A]
                [142, 87, 203, 255]

After Hiding Data:
                [R, G, B, A]  
                [140, 84, 200, 255]
                 ↑    ↑    ↑
            Changed by 2 bits max
            (Visually imperceptible)
```

**Data Structure:**
```
PNG Header + Image Data
    ↓ (hidden in LSBs)
[MEOW_STEG_V2][Size][Compressed AI Data]
```

</td>
</tr>
</table>

## ✨ Features

<table>
<tr>
<td width="50%">

### Universal Compatibility
- **Contains standard PNG data** (universal format)
- **Two ways to open**: Rename to `.png` OR file association setup
- **Cross-platform support** (Windows, Linux, macOS)
- **Web browser compatible** (after rename to `.png`)
- **Mobile app support** (rename `.meow` → `.png`)
- **Professional software** (Photoshop, GIMP - rename to `.png`)

</td>
<td width="50%">

### AI-Enhanced Capabilities
- **Steganographic storage** (invisible to standard viewers)
- **Better-for-AI metadata** (object detection, features, attention)
- **Model optimization hints** (preprocessing parameters)
- **Training data annotations** (bounding boxes, classes)
- **Performance analytics** (complexity scores, saliency maps)
- **Lossless data preservation** (survives file operations if lossless)
- **LLM context enhancement** (structured descriptions for better AI understanding)
- **Multimodal AI support** (vision-language model acceleration)

</td>
</tr>
</table>

## Format Comparison

<table>
<tr>
<th>Feature</th>
<th>MEOW Steganographic</th>
<th>PNG</th>
<th>Custom AI Formats</th>
<th>Traditional MEOW</th>
</tr>
<tr>
<td>Universal Viewer Support</td>
<td>✅ After setup (rename/association)</td>
<td>✅</td>
<td>❌ Requires special software</td>
<td>❌ Requires MEOW viewer</td>
</tr>
<tr>
<td>AI Metadata</td>
<td>✅ Rich & hidden</td>
<td>❌</td>
<td>✅ But not cross-compatible</td>
<td>✅ But not cross-compatible</td>
</tr>
<tr>
<td>File Extension Flexibility</td>
<td>✅ .meow or .png</td>
<td>✅</td>
<td>❌ Proprietary extensions</td>
<td>❌ .meow only</td>
</tr>
<tr>
<td>Cross-Platform</td>
<td>✅ Cross-platform (with setup)</td>
<td>✅</td>
<td>❌ Limited support</td>
<td>✅</td>
</tr>
<tr>
<td>AI Training Ready</td>
<td>✅ Embedded annotations</td>
<td>❌</td>
<td>✅ But compatibility issues</td>
<td>✅ But compatibility issues</td>
</tr>
<tr>
<td>Data Integrity</td>
<td>✅ Survives file operations</td>
<td>✅</td>
<td>❌ Often lost in transfers</td>
<td>❌ Lost if opened wrong</td>
</tr>
</table>

### Why Steganographic MEOW Is Awesome Here

**The Problem**: AI-enhanced formats typically sacrifice compatibility for features  
**The Solution**: Hide AI data inside universally-compatible PNG files  
**The Result**: Best of both worlds - works everywhere + AI superpowers

> **⚠️ Important**: While MEOW files contain standard PNG data, you need either:
> 1. **Rename `.meow` → `.png`** (compatibility for viewing), OR  
> 2. **Run file association scripts** (one-time setup to make `.meow` extension recognized)
> 
> Without setup, most viewers won't recognize the `.meow` extension by default. Because well, I just made it lol.

## 🛠️ How to Use

### 📦 Setup
```powershell
# Clone the repository
git clone https://github.com/kuberwastaken/meow.git

# Navigate to the directory
cd meow

# Install dependencies
pip install -r requirements.txt

# Set up file associations (optional)
windows\associate_meow.bat  # Run as administrator
```

### 🔄 Creating MEOW Files

#### Command Line - Quick Conversion
```powershell
# Convert any image to steganographic MEOW
python meow_format.py image.jpg output.meow

# Convert PNG with rich AI annotations
python convert.py image.png enhanced.meow
```

#### GUI Application - Full Featured
```powershell
# Launch the MEOW GUI with AI features
python meow_gui.py
```

### 👁️ Viewing & Testing Cross-Compatibility

#### Standard Image Viewers (2 Setup Options)
```powershell
# Option 1: Rename to .png (works instantly everywhere)
rename test.meow test.png
start test.png                    # Opens in default viewer

# Option 2: Set up file associations (makes .meow recognized)
windows\associate_meow.bat        # Run as administrator first
start test.meow                   # Now opens directly!
```

#### MEOW-Aware Applications (See AI Data)
```powershell
# Launch MEOW viewer to see hidden AI metadata
python meow_gui.py

# Run compatibility demonstration
python final_demonstration.py
```

### 🧪 Real-World Example

```powershell
# 1. Create a steganographic MEOW file
python meow_format.py "photo.jpg" "photo.meow"

# 2. Test universal compatibility - Choose your method:

# Method A: Rename to PNG (instant compatibility)
copy photo.meow photo.png          # Keep original + create PNG copy
start photo.png                    # Opens in any image viewer!

# Method B: File association setup (one-time setup)
windows\associate_meow.bat         # Run as admin (one-time setup)
start photo.meow                   # Now .meow files open directly!

# 3. Extract AI data (MEOW-aware apps see hidden metadata)
python meow_gui.py                 # Load .meow OR renamed .png - AI data intact!
```

## 🕴️ Next Steps

### File Association Setup

To make `.meow` files open directly in your system's default image viewer, run the appropriate setup script for your platform:

#### Windows
```powershell
# Run as administrator to set up file associations
windows\associate_meow.bat
```

#### macOS  
```bash
# Make executable and run
chmod +x macos/associate_meow_macos.sh
./macos/associate_meow_macos.sh
```

#### Linux/Cross-Platform
```bash
# Universal setup script that detects your OS
chmod +x scripts/associate_meow_crossplatform.sh
./scripts/associate_meow_crossplatform.sh
```

After running the appropriate script, double-clicking any `.meow` file will open it in your system's default image viewer (Paint, Preview, etc.) while preserving the hidden AI metadata for MEOW-aware applications.

**Note**: File association is optional - you can always rename `.meow` files to `.png` for instant compatibility with any image viewer.

## 🧪 Steganographic Format Specification

<table>
<tr>
<td width="60%">

### File Structure
**MEOW files ARE valid PNG files** with hidden data embedded using LSB steganography:

1. **Standard PNG Structure**: Complete, valid PNG file
2. **Hidden MEOW Header**: `MEOW_STEG_V2` (12 bytes) 
3. **Size Field**: 32-bit length of compressed data
4. **Compressed AI Data**: zlib-compressed JSON metadata

### Storage Method
- **Channels Used**: RGB only (preserves alpha transparency)
- **Bits Per Channel**: 2 LSBs modified (visually imperceptible)
- **Capacity**: 6 bits per pixel (width × height × 3 × 2 ÷ 8 bytes)
- **Compression**: zlib level 9 for maximum data density

</td>
<td width="40%">

```
📁 MEOW File Structure:
┌─────────────────────┐
│    PNG Header       │ ← Standard PNG
│                     │
│  RGB Image Data     │ ← Normal pixels +
│  (with hidden data) │   hidden AI data
│                     │   in 2 LSBs
│  PNG Footer         │ ← Standard PNG
└─────────────────────┘

🔬 Pixel-Level Storage:
Original: R[142] G[87] B[203]
Binary:   10001110 01010111 11001011

After:    R[140] G[84] B[200] 
Binary:   10001100 01010100 11001000
                ↑↑       ↑↑       ↑↑
            Hidden data bits
```

</td>
</tr>
</table>

### 📊 AI Metadata Structure
```json
{
  "version": 2,
  "features": {
    "brightness": 126.642,
    "contrast": 67.335, 
    "edge_density": 0.738,
    "mean_rgb": [126.69, 126.6, 126.64],
    "dimensions": [400, 300]
  },
  "attention_maps": {
    "avg_attention": 117.86,
    "max_attention": 255,
    "attention_peaks": 12,
    "focus_regions": [[120, 80], [250, 150]]
  },
  "ai_annotations": {
    "object_classes": ["cat", "background"],
    "bounding_boxes": [...],
    "preprocessing_params": {
      "mean_rgb": [0.485, 0.456, 0.406],
      "input_size": [224, 224],
      "normalization": "imagenet"
    },
    "llm_context": {
      "scene_description": "A domestic cat sitting on wooden surface",
      "visual_elements": ["furry texture", "natural lighting", "indoor setting"],
      "suggested_tags": ["pet", "animal", "indoor", "portrait"]
    }
  },
  "model_hints": {
    "recommended_models": ["ResNet50", "CLIP", "YOLO"],
    "complexity_score": 0.73,
    "processing_priority": "high_detail"
  }
}
```

## 🛠️ Tools & Applications

<table>
<tr>
<td width="33%" align="center">
<h3>🖼️ GUI Application</h3>
<p>Complete interface with AI metadata viewer, steganographic converter, and cross-compatibility testing</p>
</td>
<td width="33%" align="center">
<h3>🔄 Steganographic Converter</h3>
<p>Command-line tool for embedding AI data in PNG-compatible MEOW files</p>
</td>
<td width="33%" align="center">
<h3>🌐 Universal Compatibility</h3>
<p>PNG-compatible format that works in any viewer after simple setup</p>
</td>
</tr>
</table>

## 🔧 Technical Details

### Implementation
- Built with **Python 3.6+**
- Uses **Pillow/PIL** for image processing
- **NumPy** for efficient steganographic operations
- **zlib** for AI metadata compression
- **tkinter** for cross-platform GUI
- **JSON** for structured AI data storage


### Performance Characteristics
| Metric | Standard PNG | Steganographic MEOW | Difference |
|--------|-------------|-------------------|------------|
| Viewer compatibility | 100% | 100% (after setup) | Simple setup required |
| Visual quality | Perfect | Perfect | Imperceptible |
| AI data capacity | 0 bytes | 650+ bytes | Rich metadata |
| Load time | Fast | Fast | No noticeable difference |
| LLM context understanding | Basic | Better | Significantly improved |

### Real-World Applications
- **AI Training Datasets**: Embedded annotations eliminate separate metadata files
- **Computer Vision**: Pre-computed features accelerate model inference
- **Digital Asset Management**: Rich metadata without database dependency
- **Research Archives**: Self-documenting images with analysis results
- **Production Workflows**: Integration with existing tools (after setup or rename to .png)
- **LLM Vision Tasks**: Enhanced multimodal AI with embedded context
- **Automated Content Analysis**: Self-describing images for content pipelines
- **AI Model Training**: Consistent, portable annotations across platforms

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🧠 Credits & Acknowledgements

Initial idea inspired by [FaceDev](https://www.youtube.com/@FaceDevStuff), whose BRUHIFF format provided a creative starting point.

## 📜 License

This project is released under the Apache 2.0 License. See the LICENSE file for details.

---

<div align="center">

<p align="center">Made with ❤️ by <a href="https://kuber.studio/">Kuber Mehta</a></p>

<p align="center"><em>Purr-fectly optimized (I mean- as far as my ugly code takes it)</em></p>

</div>
