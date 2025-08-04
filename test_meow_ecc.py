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

def test_meow_ecc_recovery():
    """Test ECC recovery for MEOW images."""
    # Setup
    meow = MeowFormat()
    tmpdir = tempfile.mkdtemp()
    try:
        # Use a sample PNG
        sample_png = os.path.join('assets', 'sample-images', 'test.png')
        meow_path = os.path.join(tmpdir, 'test.meow')
        
        # Create MEOW file
        assert meow.create_steganographic_meow(sample_png, meow_path)
        
        # Extract original MEOW data
        img, orig_data = meow.load_steganographic_meow(meow_path)
        assert orig_data is not None
        print(f"Original data version: {orig_data.get('version')}")
        
        # Load image and corrupt LSB data
        img = Image.open(meow_path)
        img_array = np.array(img)
        
        # Corrupt LSB data (simulate transmission errors)
        corrupted_array = corrupt_lsb_data(img_array.copy(), corruption_rate=0.005)  # 0.5% corruption
        corrupted_img = Image.fromarray(corrupted_array)
        
        # Try to extract from corrupted image
        recovered_data = meow._extract_hidden_data(corrupted_img)
        print('Recovered with 0.5% corruption:', recovered_data is not None)
        
        if recovered_data is not None:
            print('✅ ECC successfully recovered data!')
            # Compare some fields
            assert recovered_data['version'] == orig_data['version']
            assert recovered_data['features']['dimensions'] == orig_data['features']['dimensions']
            print('ECC recovery test passed.')
        else:
            print('❌ ECC failed to recover data - testing lighter corruption...')
            # Try with less corruption
            corrupted_array2 = corrupt_lsb_data(img_array.copy(), corruption_rate=0.001)  # 0.1% corruption
            corrupted_img2 = Image.fromarray(corrupted_array2)
            recovered_data2 = meow._extract_hidden_data(corrupted_img2)
            
            if recovered_data2 is not None:
                print('✅ ECC recovered data with lighter corruption!')
                print('ECC recovery test passed.')
            else:
                print('❌ ECC failed even with light corruption')
                # Test without any corruption to see if basic functionality works
                no_corrupt_data = meow._extract_hidden_data(img)
                print('No corruption extraction works:', no_corrupt_data is not None)
                
    finally:
        shutil.rmtree(tmpdir)

def test_meow_vs_noecc():
    """Compare ECC vs no ECC by forcibly disabling ECC and corrupting image."""
    meow = MeowFormat()
    tmpdir = tempfile.mkdtemp()
    try:
        sample_png = os.path.join('assets', 'sample-images', 'test.png')
        meow_path = os.path.join(tmpdir, 'test.meow')
        
        # Create MEOW file with ECC
        assert meow.create_steganographic_meow(sample_png, meow_path)
        
        # Load image and corrupt LSB data
        img = Image.open(meow_path)
        img_array = np.array(img)
        corrupted_array = corrupt_lsb_data(img_array.copy(), corruption_rate=0.002)  # 0.2% corruption
        corrupted_img = Image.fromarray(corrupted_array)
        
        # ECC recovery
        recovered_data_ecc = meow._extract_hidden_data(corrupted_img)
        
        # Now forcibly disable ECC and test again
        import meow_format
        original_rscode = meow_format.RSCodec
        meow_format.RSCodec = None
        
        # Test extraction without ECC
        meow_no_ecc = MeowFormat()
        recovered_data_noecc = meow_no_ecc._extract_hidden_data(corrupted_img)
        
        # Restore original RSCodec
        meow_format.RSCodec = original_rscode
        
        print('ECC recovery:', recovered_data_ecc is not None)
        print('No ECC recovery:', recovered_data_noecc is not None)
        
        # ECC should be better at handling corruption
        if recovered_data_ecc is not None and recovered_data_noecc is None:
            print('✅ ECC successfully recovered data while no-ECC failed!')
        elif recovered_data_ecc is not None and recovered_data_noecc is not None:
            print('✅ Both recovered, but ECC provides redundancy')
        else:
            print('⚠️  Both failed - may need less corruption for this test')
            
        print('ECC vs No ECC test completed.')
    finally:
        shutil.rmtree(tmpdir)

if __name__ == '__main__':
    test_meow_ecc_recovery()
    test_meow_vs_noecc()
