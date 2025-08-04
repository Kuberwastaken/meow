import os
import shutil
import tempfile
import random
import numpy as np
from PIL import Image
from meow_format import MeowFormat

def corrupt_lsb_data(img_array, corruption_rate=0.01):
    """Corrupt LSB data in the image array to simulate steganographic data corruption."""
    height, width, channels = img_array.shape
    num_pixels_to_corrupt = int(height * width * corruption_rate)
    
    for _ in range(num_pixels_to_corrupt):
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)
        c = random.randint(0, 2)  # RGB only
        
        # Flip some LSBs
        pixel_val = img_array[y, x, c]
        # Flip 1-2 LSBs randomly
        if random.random() < 0.5:
            img_array[y, x, c] = pixel_val ^ 0x01  # Flip LSB
        else:
            img_array[y, x, c] = pixel_val ^ 0x03  # Flip 2 LSBs
    
    return img_array

def test_ecc_effectiveness():
    """Test ECC effectiveness across different corruption levels."""
    meow = MeowFormat()
    tmpdir = tempfile.mkdtemp()
    
    try:
        # Use a sample PNG
        sample_png = os.path.join('assets', 'sample-images', 'test.png')
        meow_path = os.path.join(tmpdir, 'test.meow')
        
        # Create MEOW file
        assert meow.create_steganographic_meow(sample_png, meow_path)
        
        # Load original image
        img = Image.open(meow_path)
        img_array = np.array(img)
        
        print("🧪 Testing ECC effectiveness across corruption levels:")
        print("=" * 60)
        
        corruption_rates = [0.0001, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]
        
        # Test with ECC
        print("\n📊 WITH ECC (Reed-Solomon):")
        ecc_results = []
        for rate in corruption_rates:
            corrupted_array = corrupt_lsb_data(img_array.copy(), corruption_rate=rate)
            corrupted_img = Image.fromarray(corrupted_array)
            
            recovered_data = meow._extract_hidden_data(corrupted_img)
            success = recovered_data is not None
            ecc_results.append(success)
            
            status = "✅" if success else "❌"
            print(f"{status} {rate*100:6.2f}% corruption: {'RECOVERED' if success else 'FAILED'}")
        
        # Test without ECC
        print("\n📊 WITHOUT ECC:")
        import meow_format
        original_rscode = meow_format.RSCodec
        meow_format.RSCodec = None
        
        meow_no_ecc = MeowFormat()
        no_ecc_results = []
        
        for rate in corruption_rates:
            corrupted_array = corrupt_lsb_data(img_array.copy(), corruption_rate=rate)
            corrupted_img = Image.fromarray(corrupted_array)
            
            recovered_data = meow_no_ecc._extract_hidden_data(corrupted_img)
            success = recovered_data is not None
            no_ecc_results.append(success)
            
            status = "✅" if success else "❌"
            print(f"{status} {rate*100:6.2f}% corruption: {'RECOVERED' if success else 'FAILED'}")
        
        # Restore ECC
        meow_format.RSCodec = original_rscode
        
        # Summary
        print("\n" + "=" * 60)
        print("📈 SUMMARY:")
        ecc_success_count = sum(ecc_results)
        no_ecc_success_count = sum(no_ecc_results)
        
        print(f"ECC Recovery Rate: {ecc_success_count}/{len(corruption_rates)} ({ecc_success_count/len(corruption_rates)*100:.1f}%)")
        print(f"No-ECC Recovery Rate: {no_ecc_success_count}/{len(corruption_rates)} ({no_ecc_success_count/len(corruption_rates)*100:.1f}%)")
        
        improvement = ecc_success_count - no_ecc_success_count
        if improvement > 0:
            print(f"🎉 ECC improved recovery by {improvement} scenarios!")
        elif improvement == 0:
            print("📊 ECC and no-ECC performed equally (both very robust or very fragile)")
        else:
            print("⚠️  Unexpected: No-ECC performed better (this shouldn't happen)")
            
        print(f"\n🔬 Test completed with {len(corruption_rates)} corruption levels")
        
    finally:
        shutil.rmtree(tmpdir)

if __name__ == '__main__':
    test_ecc_effectiveness()
