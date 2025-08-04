#!/usr/bin/env python3
"""
MEOW Format ECC Benchmark Test
Comprehensive testing of error correction improvements
"""

import os
import sys
import tempfile
import shutil
import time
import numpy as np
from PIL import Image
from meow_format import MeowFormat

def benchmark_ecc_improvements():
    """Benchmark ECC improvements with comprehensive tests."""
    print("🔬 MEOW Format ECC Benchmark")
    print("=" * 60)
    
    # Check for sample image
    sample_png = os.path.join('assets', 'sample-images', 'test.png')
    if not os.path.exists(sample_png):
        print("Creating test image...")
        test_img = Image.new('RGB', (200, 200), color=(128, 64, 192))
        os.makedirs('assets/sample-images', exist_ok=True)
        test_img.save(sample_png)
    
    meow = MeowFormat()
    tmpdir = tempfile.mkdtemp()
    
    results = {
        'ecc_successes': 0,
        'no_ecc_successes': 0,
        'total_tests': 0,
        'ecc_times': [],
        'no_ecc_times': []
    }
    
    try:
        # Create test MEOW file
        meow_path = os.path.join(tmpdir, 'benchmark.meow')
        print(f"\n📄 Creating test MEOW file...")
        
        meow.create_steganographic_meow(sample_png, meow_path, {
            'test_type': 'benchmark',
            'ecc_enabled': True,
            'redundancy': 'high'
        })
        
        # Load original
        img = Image.open(meow_path)
        img_array = np.array(img)
        
        print(f"✅ Test file created: {os.path.getsize(meow_path):,} bytes")
        
        # Test scenarios
        corruption_levels = [0.0001, 0.0005, 0.001, 0.002, 0.005, 0.01]
        num_trials_per_level = 3
        
        print(f"\n🧪 Running benchmark with {len(corruption_levels)} corruption levels")
        print(f"   {num_trials_per_level} trials per level = {len(corruption_levels) * num_trials_per_level} total tests")
        print(f"\n📊 Results:")
        print(f"{'Corruption':<12} {'ECC':<8} {'No-ECC':<8} {'ECC Time':<10} {'No-ECC Time'}")
        print(f"{'-'*50}")
        
        import meow_format
        original_rscode = meow_format.RSCodec
        
        for corruption_rate in corruption_levels:
            ecc_successes = 0
            no_ecc_successes = 0
            ecc_times = []
            no_ecc_times = []
            
            for trial in range(num_trials_per_level):
                # Create corrupted version
                corrupted_array = corrupt_lsb_data(img_array.copy(), corruption_rate)
                corrupted_img = Image.fromarray(corrupted_array)
                
                # Test with ECC
                start_time = time.time()
                ecc_result = meow._extract_hidden_data(corrupted_img)
                ecc_time = time.time() - start_time
                ecc_times.append(ecc_time)
                
                if ecc_result is not None:
                    ecc_successes += 1
                
                # Test without ECC
                meow_format.RSCodec = None
                meow_no_ecc = MeowFormat()
                
                start_time = time.time()
                no_ecc_result = meow_no_ecc._extract_hidden_data(corrupted_img)
                no_ecc_time = time.time() - start_time
                no_ecc_times.append(no_ecc_time)
                
                if no_ecc_result is not None:
                    no_ecc_successes += 1
                
                # Restore ECC
                meow_format.RSCodec = original_rscode
                
                results['total_tests'] += 1
            
            # Update totals
            results['ecc_successes'] += ecc_successes
            results['no_ecc_successes'] += no_ecc_successes
            results['ecc_times'].extend(ecc_times)
            results['no_ecc_times'].extend(no_ecc_times)
            
            # Print results for this corruption level
            avg_ecc_time = np.mean(ecc_times) * 1000  # Convert to ms
            avg_no_ecc_time = np.mean(no_ecc_times) * 1000
            
            print(f"{corruption_rate*100:8.2f}%    {ecc_successes}/{num_trials_per_level:<3}      {no_ecc_successes}/{num_trials_per_level:<3}      {avg_ecc_time:6.2f}ms    {avg_no_ecc_time:6.2f}ms")
        
        # Final summary
        print(f"\n" + "="*60)
        print(f"📈 BENCHMARK SUMMARY:")
        print(f"   Total tests: {results['total_tests']}")
        print(f"   ECC recovery rate: {results['ecc_successes']}/{results['total_tests']} ({results['ecc_successes']/results['total_tests']*100:.1f}%)")
        print(f"   No-ECC recovery rate: {results['no_ecc_successes']}/{results['total_tests']} ({results['no_ecc_successes']/results['total_tests']*100:.1f}%)")
        
        improvement = results['ecc_successes'] - results['no_ecc_successes']
        print(f"   Improvement: +{improvement} successful recoveries")
        
        avg_ecc_time = np.mean(results['ecc_times']) * 1000
        avg_no_ecc_time = np.mean(results['no_ecc_times']) * 1000
        print(f"   Average ECC time: {avg_ecc_time:.2f}ms")
        print(f"   Average No-ECC time: {avg_no_ecc_time:.2f}ms")
        print(f"   Time overhead: {((avg_ecc_time / avg_no_ecc_time) - 1) * 100:.1f}%")
        
        # Verdict
        if improvement > 0:
            print(f"\n🎉 ECC PROVIDES SIGNIFICANT IMPROVEMENT!")
            print(f"   ✅ {improvement} more successful recoveries")
            print(f"   ✅ Better resilience to data corruption")
            if avg_ecc_time < avg_no_ecc_time * 2:
                print(f"   ✅ Reasonable performance overhead")
        
        print(f"\n🔬 Benchmark completed successfully!")
        
    finally:
        shutil.rmtree(tmpdir)

def corrupt_lsb_data(img_array, corruption_rate):
    """Corrupt LSB data in image array."""
    height, width, channels = img_array.shape
    num_pixels = int(height * width * corruption_rate)
    
    for _ in range(num_pixels):
        y = np.random.randint(0, height)
        x = np.random.randint(0, width)
        c = np.random.randint(0, 3)  # RGB only
        
        # Flip 1-2 LSBs
        img_array[y, x, c] ^= np.random.randint(1, 4)
    
    return img_array

if __name__ == '__main__':
    benchmark_ecc_improvements()
