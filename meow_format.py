"""
MEOW File Format Implementation
Steganographic cross-compatible image format that works everywhere
"""

import struct
import json
import datetime
import zlib
import io
import os
import sys
from typing import Tuple, Optional, Dict, List, Union
from PIL import Image
import numpy as np
from dataclasses import dataclass, asdict

# Error correction
try:
    from reedsolo import RSCodec
except ImportError:
    RSCodec = None  # Will gracefully fallback without ECC


@dataclass
class AIMetadata:
    """AI-specific metadata structure"""
    # Semantic annotations
    object_classes: List[str] = None
    bounding_boxes: List[Dict] = None
    segmentation_masks: Dict = None
    
    # Attention and saliency
    attention_maps: Dict = None
    saliency_regions: List[Dict] = None
    
    # Model optimization hints
    optimal_input_size: Tuple[int, int] = None
    preprocessing_params: Dict = None
    feature_importance: Dict = None
    
    # Content analysis
    complexity_map: Dict = None
    texture_analysis: Dict = None
    edge_density: float = None
    
    # AI Generation Detection
    ai_generated: bool = None
    generation_service: str = None  # e.g., "DALL-E", "Midjourney", "Stable Diffusion", "ChatGPT", etc.
    generation_platform: str = None  # e.g., "OpenAI", "Discord", "RunwayML", "Hugging Face", etc.
    generation_time: str = None  # ISO datetime when generated
    generation_prompt: str = None  # Original text prompt used
    has_reference_image: bool = None  # Whether a reference/seed image was used
    reference_image_url: str = None  # URL or path to reference image if available
    model_version: str = None  # e.g., "DALL-E 3", "Midjourney v6", "SD XL 1.0", etc.
    generation_settings: Dict = None  # Model-specific settings (steps, guidance, etc.)
    watermark_detected: bool = None  # Whether AI watermark was detected
    confidence_score: float = None  # AI detection confidence (0.0-1.0)


class MeowFormat:
    """
    Steganographic MEOW format - True cross-compatibility
    Creates .meow files that work in any image viewer
    """
    
    MAGIC_HEADER = b"MEOW_STEG_V2"  # 12 bytes
    VERSION = 2
    
    def __init__(self):
        self.ai_metadata = AIMetadata()
        self.metadata = {}
        
    def png_to_meow(self, input_path: str, output_path: str = None) -> bool:
        """Convert PNG to steganographic MEOW format"""
        try:
            if output_path is None:
                output_path = input_path.rsplit('.', 1)[0] + '.meow'
            
            # Create enhanced AI annotations
            ai_annotations = {
                'created_from': os.path.basename(input_path),
                'creation_date': datetime.datetime.now().isoformat(),
                'software': f'MEOW Python Implementation v{self.VERSION}',
                'format': 'Steganographic MEOW',
                'ai_optimized': True
            }
            
            return self.create_steganographic_meow(input_path, output_path, ai_annotations)
            
        except Exception as e:
            print(f"Error converting to MEOW: {e}")
            return False
    
    def meow_to_image(self, input_path: str) -> Optional[Image.Image]:
        """Load MEOW file as PIL Image"""
        try:
            img, meow_data = self.load_steganographic_meow(input_path)
            if img:
                # Store metadata for later access
                if meow_data:
                    self.metadata = meow_data.get('ai_annotations', {})
                    # Convert to AIMetadata
                    if 'features' in meow_data:
                        features = meow_data['features']
                        self.ai_metadata.edge_density = features.get('edge_density')
                        self.ai_metadata.complexity_map = {'brightness': features.get('brightness')}
            return img
        except Exception as e:
            print(f"Error loading MEOW: {e}")
            return None
    
    def get_file_info(self, file_path: str) -> Optional[Dict]:
        """Get information about a MEOW file"""
        try:
            if not os.path.exists(file_path):
                return None
                
            img, meow_data = self.load_steganographic_meow(file_path)
            if not img:
                return None
            
            file_size = os.path.getsize(file_path)
            width, height = img.size
            
            return {
                'format': 'Steganographic MEOW',
                'width': width,
                'height': height,
                'pixels': width * height,
                'file_size': file_size,
                'pixel_data_size': width * height * 4,  # RGBA
                'metadata_size': len(json.dumps(meow_data).encode()) if meow_data else 0,
                'ai_enhanced': meow_data is not None,
                'hidden_data': bool(meow_data)
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None    
            
    def create_steganographic_meow(self, image_path: str, output_path: str = None,
                                 ai_annotations: Dict = None) -> bool:
        """Create a .meow file that's actually a PNG with hidden MEOW data"""
        try:
            # Load and prepare image
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            if output_path is None:
                output_path = image_path.rsplit('.', 1)[0] + '.meow'
            
            # Ensure .meow extension
            if not output_path.lower().endswith('.meow'):
                output_path = output_path.rsplit('.', 1)[0] + '.meow'
            
            # Prepare MEOW data for hiding
            meow_data = self._prepare_meow_data(img, ai_annotations)
            
            # Hide data in image using steganography
            stego_img = self._hide_data_in_image(img, meow_data)
            
            # Save as PNG but with .meow extension
            stego_img.save(output_path, format='PNG', optimize=True)
            
            print(f"✅ Created steganographic MEOW file: {output_path}")
            print(f"📱 File opens as PNG in ANY viewer despite .meow extension")
            print(f"🤖 MEOW data hidden in pixel LSBs")
            print(f"📊 Hidden data size: {len(meow_data)} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating steganographic MEOW: {e}")
            return False
    
    def load_steganographic_meow(self, file_path: str, 
                               extract_meow_data: bool = True) -> Tuple[Image.Image, Optional[Dict]]:
        """Load steganographic MEOW file"""
        try:
            # Load as standard PNG (always works)
            img = Image.open(file_path)
            
            if not extract_meow_data:
                return img, None
            
            # Extract hidden MEOW data
            meow_data = self._extract_hidden_data(img)
            
            return img, meow_data
            
        except Exception as e:
            print(f"Error loading steganographic MEOW: {e}")
            return None, None
    
    def _prepare_meow_data(self, img: Image.Image, ai_annotations: Dict = None) -> bytes:
        """Prepare MEOW data for steganographic hiding, with ECC and redundancy"""
        try:
            # Generate AI features
            features = self._generate_features(img)
            
            # Generate attention maps  
            attention_maps = self._generate_attention_maps(img)
            
            # Build complete MEOW data structure
            meow_structure = {
                'version': self.VERSION,
                'features': features,
                'attention_maps': attention_maps,
                'ai_annotations': ai_annotations or {},
                'creation_date': datetime.datetime.now().isoformat()
            }
            
            # Serialize and compress
            json_data = json.dumps(meow_structure, separators=(',', ':')).encode('utf-8')
            compressed_data = zlib.compress(json_data, level=9)
            
            # ECC encoding (Reed-Solomon)
            if RSCodec:
                # Add redundancy: 32 bytes ECC
                rsc = RSCodec(32)
                ecc_data = rsc.encode(compressed_data)
            else:
                ecc_data = compressed_data
            
            # Create final structure: header + size + ECC data
            size_bytes = struct.pack('<I', len(ecc_data))
            # Redundant header: repeat header twice for robustness
            return self.MAGIC_HEADER + self.MAGIC_HEADER + size_bytes + ecc_data
            
        except Exception as e:
            print(f"Error preparing MEOW data: {e}")
            return b""
    
    def _hide_data_in_image(self, img: Image.Image, data: bytes) -> Image.Image:
        """Hide data in image using LSB steganography"""
        try:
            # Convert to numpy array
            img_array = np.array(img)
            height, width, channels = img_array.shape
            
            # Calculate maximum capacity (2 bits per RGB channel = 6 bits per pixel)
            max_capacity = (width * height * 3 * 2) // 8  # 3 RGB channels, 2 bits each
            
            if len(data) > max_capacity:
                raise ValueError(f"Data too large: {len(data)} bytes > {max_capacity} bytes capacity")
            
            # Convert data to binary string
            binary_data = ''.join(format(byte, '08b') for byte in data)
            
            # Add padding to align with 6-bit boundaries
            while len(binary_data) % 6 != 0:
                binary_data += '0'
            
            data_index = 0
            
            # Hide data in RGB channels (skip alpha)
            for y in range(height):
                for x in range(width):
                    if data_index >= len(binary_data):
                        break
                        
                    pixel = img_array[y, x]
                    
                    # Process RGB channels (skip alpha channel 3)
                    for c in range(3):  # R, G, B only
                        if data_index + 1 < len(binary_data):
                            # Clear the 2 LSBs and set new values
                            img_array[y, x, c] = (pixel[c] & 0xFC) | int(binary_data[data_index:data_index+2], 2)
                            data_index += 2
                        elif data_index < len(binary_data):
                            # Handle single remaining bit
                            img_array[y, x, c] = (pixel[c] & 0xFE) | int(binary_data[data_index], 2)
                            data_index += 1
            
            return Image.fromarray(img_array, 'RGBA')
            
        except Exception as e:
            print(f"Error hiding data: {e}")
            return img
    
    def _extract_hidden_data(self, img: Image.Image) -> Optional[Dict]:
        """Extract hidden MEOW data from image, with ECC and redundancy"""
        try:
            # Convert to numpy array
            img_array = np.array(img)
            height, width, channels = img_array.shape
            
            # Extract binary data from RGB LSBs
            binary_data = ""
            
            for y in range(height):
                for x in range(width):
                    pixel = img_array[y, x]
                    
                    # Extract 2 bits from each RGB channel
                    for c in range(3):  # R, G, B only
                        binary_data += format(pixel[c] & 0x03, '02b')  # Get 2 LSBs
            
            # Convert binary string back to bytes
            extracted_bytes = bytearray()
            for i in range(0, len(binary_data), 8):
                if i + 8 <= len(binary_data):
                    byte_str = binary_data[i:i+8]
                    extracted_bytes.append(int(byte_str, 2))
            
            # Look for MEOW magic header (redundant)
            extracted_data = bytes(extracted_bytes)
            magic_pos = extracted_data.find(self.MAGIC_HEADER + self.MAGIC_HEADER)
            
            if magic_pos == -1:
                # Fallback: try single header
                magic_pos = extracted_data.find(self.MAGIC_HEADER)
                if magic_pos == -1:
                    return None  # No MEOW data found
                start_pos = magic_pos + len(self.MAGIC_HEADER)
            else:
                start_pos = magic_pos + 2 * len(self.MAGIC_HEADER)
            
            if start_pos + 4 > len(extracted_data):
                return None
            
            size = struct.unpack('<I', extracted_data[start_pos:start_pos+4])[0]
            ecc_start = start_pos + 4
            
            if ecc_start + size > len(extracted_data):
                return None
            
            ecc_data = extracted_data[ecc_start:ecc_start+size]
            
            # ECC decode
            if RSCodec:
                rsc = RSCodec(32)
                try:
                    decoded_result = rsc.decode(ecc_data)
                    # reedsolo returns (data, ecc) tuple
                    if isinstance(decoded_result, tuple):
                        compressed_data = decoded_result[0]
                    else:
                        compressed_data = decoded_result
                except Exception as e:
                    print(f"ECC decode failed: {e}")
                    return None
            else:
                compressed_data = ecc_data
            
            # Decompress and parse JSON
            json_data = zlib.decompress(compressed_data)
            meow_structure = json.loads(json_data.decode('utf-8'))
            
            return meow_structure
            
        except Exception as e:
            print(f"Error extracting hidden data: {e}")
            return None
    
    def _generate_features(self, img: Image.Image) -> Dict:
        """Generate AI-relevant features from image"""
        try:
            # Convert to RGB for analysis
            if img.mode != 'RGB':
                rgb_img = img.convert('RGB')
            else:
                rgb_img = img
            
            img_array = np.array(rgb_img)
            
            # Basic image statistics
            brightness = float(np.mean(img_array))
            contrast = float(np.std(img_array))
            
            # Edge density calculation
            gray = np.mean(img_array, axis=2)
            edges_x = np.abs(np.diff(gray, axis=1))
            edges_y = np.abs(np.diff(gray, axis=0))
            edge_density = float(np.mean(edges_x) + np.mean(edges_y))
            
            # Color analysis
            mean_rgb = [float(np.mean(img_array[:, :, i])) for i in range(3)]
            std_rgb = [float(np.std(img_array[:, :, i])) for i in range(3)]
            
            return {
                'brightness': brightness,
                'contrast': contrast,
                'edge_density': edge_density,
                'mean_rgb': mean_rgb,
                'std_rgb': std_rgb,
                'dimensions': list(img.size)
            }
            
        except Exception as e:
            print(f"Error generating features: {e}")
            return {}
    
    def _generate_attention_maps(self, img: Image.Image) -> Dict:
        """Generate simple attention maps for AI processing"""
        try:
            # Convert to grayscale for analysis
            gray_img = img.convert('L')
            img_array = np.array(gray_img)
            
            # Simple saliency based on gradient magnitude
            grad_x = np.abs(np.diff(img_array, axis=1))
            grad_y = np.abs(np.diff(img_array, axis=0))
            
            # Pad to match original size
            grad_x = np.pad(grad_x, ((0, 0), (0, 1)), mode='edge')
            grad_y = np.pad(grad_y, ((0, 1), (0, 0)), mode='edge')
            
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            
            # Normalize to 0-255 range
            if gradient_magnitude.max() > 0:
                attention_map = (gradient_magnitude / gradient_magnitude.max() * 255).astype(np.uint8)
            else:
                attention_map = np.zeros_like(img_array, dtype=np.uint8)
            
            # Find high attention regions (simple thresholding)
            threshold = np.percentile(attention_map, 90)
            high_attention_coords = np.argwhere(attention_map > threshold)
            
            return {
                'attention_peaks': len(high_attention_coords),
                'avg_attention': float(np.mean(attention_map)),
                'max_attention': float(np.max(attention_map)),
                'attention_std': float(np.std(attention_map))
            }
            
        except Exception as e:
            print(f"Error generating attention maps: {e}")
            return {}
    
    def get_ai_metadata(self) -> AIMetadata:
        """Get AI metadata from loaded file"""
        return self.ai_metadata


def smart_fallback_loader(file_path: str) -> Optional[Image.Image]:
    """Smart loader that can handle both MEOW and regular image files"""
    try:
        # Try loading as MEOW first
        meow = MeowFormat()
        img = meow.meow_to_image(file_path)
        if img:
            return img
        
        # Fallback to regular image loading
        return Image.open(file_path)
        
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python meow_format.py <image_path> [output_path]")
        print("Converts image to steganographic MEOW format")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create steganographic MEOW
    meow = MeowFormat()
    
    # Add AI annotations
    ai_annotations = {
        'source': 'command_line_conversion',
        'processing_date': datetime.datetime.now().isoformat(),
        'ai_enhanced': True
    }
    
    success = meow.create_steganographic_meow(input_path, output_path, ai_annotations)
    
    if success:
        if output_path is None:
            output_path = input_path.rsplit('.', 1)[0] + '.meow'
        
        print(f"\n🎉 Successfully created: {output_path}")
        print("🔍 Testing file...")
        
        # Test loading
        loaded_img, meow_data = meow.load_steganographic_meow(output_path)
        if loaded_img and meow_data:
            print("✅ File verified - MEOW data successfully extracted")
            print(f"📊 Hidden features: {list(meow_data.get('features', {}).keys())}")
            print(f"🤖 AI annotations: {list(meow_data.get('ai_annotations', {}).keys())}")
        else:
            print("❌ Verification failed")
    else:
        print("❌ Failed to create MEOW file")
