#!/usr/bin/env python3
"""
Icon Generation Script for BatchWatermark Application

This script converts PNG icon files to Windows ICO and macOS ICNS formats
for proper application packaging and distribution.
"""

import os
import sys
from pathlib import Path
from PIL import Image

def generate_ico_icon(assets_dir, output_path):
    """Generate Windows ICO icon from PNG files."""
    # Common ICO sizes
    ico_sizes = [16, 32, 48, 256]
    images = []
    
    print("🔍 Collecting PNG icons for ICO generation...")
    
    for size in ico_sizes:
        icon_path = assets_dir / f"icon_{size}.png"
        if icon_path.exists():
            print(f"   ✅ Found {size}x{size} icon")
            img = Image.open(icon_path)
            if img.size != (size, size):
                img = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(img)
        else:
            print(f"   ⚠️  Missing {size}x{size} icon, creating from largest available")
            # Find largest available icon and resize
            largest_icon = None
            for check_size in [1024, 512, 256, 128, 64]:
                check_path = assets_dir / f"icon_{check_size}.png"
                if check_path.exists():
                    largest_icon = check_path
                    break
            
            if largest_icon:
                img = Image.open(largest_icon)
                img = img.resize((size, size), Image.Resampling.LANCZOS)
                images.append(img)
    
    if images:
        print(f"💾 Saving ICO icon to {output_path}")
        images[0].save(output_path, format='ICO', sizes=[(img.width, img.height) for img in images])
        print("✅ ICO icon generated successfully!")
        return True
    else:
        print("❌ No suitable icons found for ICO generation")
        return False

def generate_icns_icon_alternative(assets_dir, output_path):
    """Generate macOS ICNS icon using PNG to ICNS conversion."""
    try:
        import subprocess
        
        # Check if iconutil is available (macOS)
        if sys.platform == 'darwin':
            print("🍎 Using macOS iconutil for ICNS generation...")
            
            # Create iconset directory
            iconset_dir = assets_dir / "app_icon.iconset"
            iconset_dir.mkdir(exist_ok=True)
            
            # Required ICNS sizes and their corresponding names
            icns_mapping = {
                'icon_16x16.png': 16,
                'icon_16x16@2x.png': 32,
                'icon_32x32.png': 32,
                'icon_32x32@2x.png': 64,
                'icon_128x128.png': 128,
                'icon_128x128@2x.png': 256,
                'icon_256x256.png': 256,
                'icon_256x256@2x.png': 512,
                'icon_512x512.png': 512,
                'icon_512x512@2x.png': 1024,
            }
            
            print("🔄 Creating iconset directory structure...")
            
            for iconset_name, source_size in icns_mapping.items():
                source_path = assets_dir / f"icon_{source_size}.png"
                target_path = iconset_dir / iconset_name
                
                if source_path.exists():
                    print(f"   ✅ Copying {source_size}x{source_size} → {iconset_name}")
                    img = Image.open(source_path)
                    img.save(target_path, format='PNG')
                else:
                    # Find largest available and resize
                    for check_size in [1024, 512, 256, 128, 64, 48, 32, 16]:
                        check_path = assets_dir / f"icon_{check_size}.png"
                        if check_path.exists():
                            print(f"   🔄 Resizing {check_size}x{check_size} → {iconset_name}")
                            img = Image.open(check_path)
                            img = img.resize((source_size, source_size), Image.Resampling.LANCZOS)
                            img.save(target_path, format='PNG')
                            break
            
            # Generate ICNS using iconutil
            print(f"🛠️  Running iconutil to create {output_path}")
            result = subprocess.run([
                'iconutil', '-c', 'icns', str(iconset_dir), '-o', str(output_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ ICNS icon generated successfully!")
                # Clean up iconset directory
                import shutil
                shutil.rmtree(iconset_dir)
                return True
            else:
                print(f"❌ iconutil failed: {result.stderr}")
                return False
        else:
            print("⚠️  macOS iconutil not available on this platform")
            return generate_icns_fallback(assets_dir, output_path)
            
    except ImportError:
        print("⚠️  subprocess not available, using fallback method")
        return generate_icns_fallback(assets_dir, output_path)
    except Exception as e:
        print(f"❌ Error during ICNS generation: {e}")
        return generate_icns_fallback(assets_dir, output_path)

def generate_icns_fallback(assets_dir, output_path):
    """Fallback method for ICNS generation using PIL directly."""
    print("🔄 Using fallback ICNS generation method...")
    
    # Use the largest available PNG as a temporary ICNS
    largest_size = 0
    largest_icon = None
    
    for size in [1024, 512, 256, 128, 64, 48, 32, 16]:
        icon_path = assets_dir / f"icon_{size}.png"
        if icon_path.exists() and size > largest_size:
            largest_size = size
            largest_icon = icon_path
    
    if largest_icon:
        print(f"📋 Copying {largest_icon.name} as ICNS file")
        import shutil
        shutil.copy2(largest_icon, output_path.with_suffix('.png'))
        print(f"⚠️  Created {output_path.with_suffix('.png')} instead of ICNS")
        print("   Note: For proper ICNS support, run this script on macOS")
        return True
    else:
        print("❌ No suitable icons found for ICNS generation")
        return False

def main():
    """Main icon generation function."""
    print("🎨 BatchWatermark Icon Generation")
    print("=" * 40)
    
    # Get project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    assets_dir = project_root / "assets"
    
    print(f"📁 Assets directory: {assets_dir}")
    
    if not assets_dir.exists():
        print("❌ Assets directory not found!")
        sys.exit(1)
    
    # Check for required PNG icons
    required_found = False
    for size in [16, 32, 48, 64, 128, 256, 512, 1024]:
        icon_path = assets_dir / f"icon_{size}.png"
        if icon_path.exists():
            required_found = True
            break
    
    if not required_found:
        print("❌ No PNG icon files found in assets directory!")
        print("   Expected files: icon_16.png, icon_32.png, icon_48.png, etc.")
        sys.exit(1)
    
    success_count = 0
    
    # Generate ICO icon for Windows
    ico_path = assets_dir / "app_icon.ico"
    print(f"\n🪟 Generating Windows ICO icon...")
    if generate_ico_icon(assets_dir, ico_path):
        success_count += 1
    
    # Generate ICNS icon for macOS
    icns_path = assets_dir / "app_icon.icns"
    print(f"\n🍎 Generating macOS ICNS icon...")
    if generate_icns_icon_alternative(assets_dir, icns_path):
        success_count += 1
    
    # Summary
    print(f"\n📊 Icon Generation Summary")
    print(f"   ✅ Successfully generated: {success_count}/2 icon formats")
    
    if success_count == 2:
        print("🎉 All icon formats generated successfully!")
        print(f"   Windows ICO: {ico_path}")
        print(f"   macOS ICNS: {icns_path}")
    elif success_count == 1:
        print("⚠️  Partial success - some icon formats may need manual creation")
    else:
        print("❌ Icon generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()