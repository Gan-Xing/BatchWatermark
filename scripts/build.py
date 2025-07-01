#!/usr/bin/env python3
"""
BatchWatermark Build Script
自动化构建脚本，用于打包BatchWatermark应用程序
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import argparse

class BatchWatermarkBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.main_script = self.project_root / "batch_watermark.py"
        
        # 检测操作系统
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_macos = self.system == "darwin"
        self.is_linux = self.system == "linux"
        
        print(f"🔍 检测到操作系统: {platform.system()}")
        print(f"📁 项目根目录: {self.project_root}")
    
    def clean_build_files(self):
        """清理之前的构建文件"""
        print("🧹 清理构建文件...")
        
        # 清理目录
        for directory in [self.dist_dir, self.build_dir]:
            if directory.exists():
                shutil.rmtree(directory)
                print(f"   删除目录: {directory}")
        
        # 清理spec文件
        for spec_file in self.project_root.glob("*.spec"):
            spec_file.unlink()
            print(f"   删除文件: {spec_file}")
    
    def check_dependencies(self):
        """检查构建依赖"""
        print("📋 检查依赖...")
        
        # 检查主脚本
        if not self.main_script.exists():
            print(f"❌ 未找到主脚本: {self.main_script}")
            return False
        
        # 检查requirements.txt
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print(f"⚠️ 未找到requirements.txt文件")
        
        # 检查PyInstaller
        try:
            subprocess.run([sys.executable, "-c", "import PyInstaller"], 
                         check=True, capture_output=True)
            print("✅ PyInstaller已安装")
        except subprocess.CalledProcessError:
            print("❌ PyInstaller未安装，请运行: pip install pyinstaller")
            return False
        
        # 检查其他依赖
        dependencies = ['PIL', 'openpyxl', 'tkinter']
        for dep in dependencies:
            try:
                subprocess.run([sys.executable, "-c", f"import {dep}"], 
                             check=True, capture_output=True)
                print(f"✅ {dep}已安装")
            except subprocess.CalledProcessError:
                print(f"❌ {dep}未安装")
                return False
        
        return True
    
    def get_icon_path(self):
        """获取图标文件路径，智能检测并提供详细反馈"""
        assets_dir = self.project_root / "assets"
        
        print("🎨 检测应用程序图标...")
        
        # 检查assets目录是否存在
        if not assets_dir.exists():
            print(f"❌ Assets目录不存在: {assets_dir}")
            print("💡 建议:")
            print("   1. 创建assets目录")
            print("   2. 运行 python scripts/generate_icons.py 生成图标")
            return None
        
        # 根据平台确定优先图标格式
        if self.is_windows:
            primary_icon = assets_dir / "app_icon.ico"
            fallback_icons = [
                assets_dir / "icon_256.png",
                assets_dir / "icon_128.png",
                assets_dir / "icon_64.png",
                assets_dir / "appstore.png"
            ]
            platform_name = "Windows"
        elif self.is_macos:
            primary_icon = assets_dir / "app_icon.icns"
            fallback_icons = [
                assets_dir / "icon_512.png",
                assets_dir / "icon_256.png",
                assets_dir / "icon_128.png",
                assets_dir / "appstore.png"
            ]
            platform_name = "macOS"
        else:
            # Linux - 使用PNG即可
            primary_icon = assets_dir / "icon_256.png"
            fallback_icons = [
                assets_dir / "icon_512.png",
                assets_dir / "icon_128.png",
                assets_dir / "icon_64.png",
                assets_dir / "appstore.png"
            ]
            platform_name = "Linux"
        
        # 检查主要图标文件
        if primary_icon.exists():
            file_size = primary_icon.stat().st_size / 1024  # KB
            print(f"✅ 找到{platform_name}图标: {primary_icon.name} ({file_size:.1f} KB)")
            return str(primary_icon)
        
        # 检查备选图标
        print(f"⚠️ 未找到{platform_name}专用图标 ({primary_icon.name})")
        
        for fallback in fallback_icons:
            if fallback.exists():
                file_size = fallback.stat().st_size / 1024  # KB
                print(f"🔄 使用备选图标: {fallback.name} ({file_size:.1f} KB)")
                print(f"💡 提示: 运行 python scripts/generate_icons.py 生成优化的{platform_name}图标")
                return str(fallback)
        
        # 没有找到任何图标
        print("❌ 未找到任何可用的图标文件")
        print("📋 可用图标检查结果:")
        
        # 列出assets目录中的所有文件
        if assets_dir.exists():
            icon_files = list(assets_dir.glob("*.png")) + list(assets_dir.glob("*.ico")) + list(assets_dir.glob("*.icns"))
            if icon_files:
                print("   发现的图标文件:")
                for icon_file in sorted(icon_files):
                    file_size = icon_file.stat().st_size / 1024  # KB
                    print(f"     📄 {icon_file.name} ({file_size:.1f} KB)")
            else:
                print("   ❌ assets目录中没有图标文件")
        
        print("\n🛠️ 图标问题解决方案:")
        print("   1. 运行图标生成脚本:")
        print("      python scripts/generate_icons.py")
        print("   2. 手动放置图标文件到assets目录:")
        if self.is_windows:
            print("      assets/app_icon.ico (推荐)")
            print("      assets/icon_256.png (备选)")
        elif self.is_macos:
            print("      assets/app_icon.icns (推荐)")
            print("      assets/icon_512.png (备选)")
        else:
            print("      assets/icon_256.png (推荐)")
        print("   3. 查看图标制作指南: ICON_GUIDE.md")
        
        return None
    
    def validate_icon_quality(self, icon_path):
        """验证图标文件质量和兼容性"""
        if not icon_path or not Path(icon_path).exists():
            return True  # Skip validation if no icon
        
        try:
            from PIL import Image
            
            icon_file = Path(icon_path)
            print(f"🔍 验证图标质量: {icon_file.name}")
            
            # 检查文件大小
            file_size_kb = icon_file.stat().st_size / 1024
            if file_size_kb > 500:  # 500KB
                print(f"⚠️ 图标文件较大 ({file_size_kb:.1f} KB)，可能影响应用程序体积")
            
            # 尝试打开图像文件进行验证
            if icon_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                with Image.open(icon_path) as img:
                    width, height = img.size
                    print(f"   图像尺寸: {width}x{height}")
                    
                    # 检查图像是否为正方形
                    if width != height:
                        print(f"⚠️ 图标不是正方形 ({width}x{height})，建议使用正方形图标")
                    
                    # 检查推荐尺寸
                    recommended_sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
                    if width not in recommended_sizes:
                        closest_size = min(recommended_sizes, key=lambda x: abs(x - width))
                        print(f"💡 建议使用标准尺寸，最接近的推荐尺寸: {closest_size}x{closest_size}")
                    
                    # 检查透明度
                    if img.mode in ['RGBA', 'LA'] or 'transparency' in img.info:
                        print("✅ 图标支持透明背景")
                    else:
                        print("💡 建议使用透明背景的图标以获得更好效果")
            
            elif icon_file.suffix.lower() == '.ico':
                print("✅ ICO格式适用于Windows应用程序")
            
            elif icon_file.suffix.lower() == '.icns':
                print("✅ ICNS格式适用于macOS应用程序")
            
            return True
            
        except ImportError:
            print("⚠️ PIL未安装，跳过图标质量验证")
            return True
        except Exception as e:
            print(f"⚠️ 图标验证时出现问题: {e}")
            print("   构建将继续，但图标可能存在问题")
            return True
    
    def build_application(self, mode="onedir", with_console=False):
        """构建应用程序"""
        print(f"🔨 开始构建应用程序 (模式: {mode})...")
        
        # 基本PyInstaller命令
        cmd = [
            "pyinstaller",
            f"--{mode}",
            "--name=BatchWatermark",
            "--clean",
        ]
        
        # 添加窗口模式（无控制台）
        if not with_console:
            cmd.append("--windowed")
        
        # 添加图标
        icon_path = self.get_icon_path()
        if icon_path:
            # 验证图标质量
            self.validate_icon_quality(icon_path)
            cmd.extend(["--icon", icon_path])
        else:
            print("⚠️ 将使用默认系统图标")
            print("💡 提示: 运行 python scripts/generate_icons.py 创建专用图标")
        
        # 添加数据文件（如果需要）
        # cmd.extend(["--add-data", "assets;assets"])
        
        # 排除不需要的模块
        exclude_modules = [
            "matplotlib", "numpy", "pandas", "scipy",
            "IPython", "jupyter", "notebook"
        ]
        for module in exclude_modules:
            cmd.extend(["--exclude-module", module])
        
        # 添加主脚本
        cmd.append(str(self.main_script))
        
        print(f"📝 构建命令: {' '.join(cmd)}")
        
        try:
            # 执行构建
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ 构建成功完成!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 构建失败:")
            print(f"   错误代码: {e.returncode}")
            print(f"   错误输出: {e.stderr}")
            return False
    
    def create_distribution_package(self):
        """创建分发包"""
        print("📦 创建分发包...")
        
        # 确定分发目录名称
        if self.is_windows:
            dist_name = "BatchWatermark-Windows"
        elif self.is_macos:
            dist_name = "BatchWatermark-macOS"
        else:
            dist_name = "BatchWatermark-Linux"
        
        app_dir = self.dist_dir / "BatchWatermark"
        dist_package_dir = self.dist_dir / dist_name
        
        if not app_dir.exists():
            print(f"❌ 未找到构建的应用程序目录: {app_dir}")
            return False
        
        # 复制应用程序文件
        if dist_package_dir.exists():
            shutil.rmtree(dist_package_dir)
        
        shutil.copytree(app_dir, dist_package_dir)
        
        # 复制文档文件
        docs_to_copy = [
            "README.md", "README_CN.md", 
            "USER_GUIDE.md", "USER_GUIDE_CN.md",
            "requirements.txt"
        ]
        
        for doc in docs_to_copy:
            doc_path = self.project_root / doc
            if doc_path.exists():
                shutil.copy2(doc_path, dist_package_dir)
                print(f"   复制文档: {doc}")
        
        print(f"✅ 分发包创建完成: {dist_package_dir}")
        return True
    
    def create_archive(self):
        """创建压缩包"""
        print("🗜️ 创建压缩包...")
        
        # 确定压缩包名称
        if self.is_windows:
            dist_name = "BatchWatermark-Windows"
            archive_format = "zip"
        elif self.is_macos:
            dist_name = "BatchWatermark-macOS"
            archive_format = "gztar"  # .tar.gz
        else:
            dist_name = "BatchWatermark-Linux"
            archive_format = "gztar"  # .tar.gz
        
        dist_package_dir = self.dist_dir / dist_name
        
        if not dist_package_dir.exists():
            print(f"❌ 未找到分发包目录: {dist_package_dir}")
            return False
        
        # 创建压缩包
        archive_path = shutil.make_archive(
            str(self.dist_dir / dist_name),
            archive_format,
            str(self.dist_dir),
            dist_name
        )
        
        print(f"✅ 压缩包创建完成: {archive_path}")
        return True
    
    def print_build_summary(self):
        """打印构建摘要"""
        print("\n" + "="*50)
        print("📊 构建摘要")
        print("="*50)
        
        if self.dist_dir.exists():
            print(f"📁 分发目录: {self.dist_dir}")
            
            # 列出生成的文件
            for item in self.dist_dir.iterdir():
                if item.is_file():
                    size = item.stat().st_size / (1024 * 1024)  # MB
                    print(f"   📄 {item.name} ({size:.1f} MB)")
                elif item.is_dir():
                    # 计算目录大小
                    total_size = sum(
                        f.stat().st_size for f in item.rglob('*') if f.is_file()
                    ) / (1024 * 1024)  # MB
                    print(f"   📁 {item.name}/ ({total_size:.1f} MB)")
        
        print("\n🎉 构建完成！")
        print("💡 使用说明:")
        print("   - 分发目录包含完整的应用程序")
        print("   - 压缩包可直接分发给最终用户")
        print("   - 用户解压后直接运行主程序即可")

def main():
    parser = argparse.ArgumentParser(description="BatchWatermark 构建脚本")
    parser.add_argument(
        "--mode", 
        choices=["onedir", "onefile"], 
        default="onedir",
        help="构建模式 (默认: onedir)"
    )
    parser.add_argument(
        "--console", 
        action="store_true",
        help="保留控制台窗口（用于调试）"
    )
    parser.add_argument(
        "--no-clean", 
        action="store_true",
        help="不清理之前的构建文件"
    )
    parser.add_argument(
        "--no-archive", 
        action="store_true",
        help="不创建压缩包"
    )
    
    args = parser.parse_args()
    
    # 创建构建器
    builder = BatchWatermarkBuilder()
    
    print("🚀 BatchWatermark 自动化构建脚本")
    print("="*50)
    
    # 清理构建文件
    if not args.no_clean:
        builder.clean_build_files()
    
    # 检查依赖
    if not builder.check_dependencies():
        print("❌ 依赖检查失败，请解决上述问题后重试")
        sys.exit(1)
    
    # 构建应用程序
    if not builder.build_application(mode=args.mode, with_console=args.console):
        print("❌ 应用程序构建失败")
        sys.exit(1)
    
    # 创建分发包
    if not builder.create_distribution_package():
        print("❌ 分发包创建失败")
        sys.exit(1)
    
    # 创建压缩包
    if not args.no_archive:
        if not builder.create_archive():
            print("❌ 压缩包创建失败")
            sys.exit(1)
    
    # 打印摘要
    builder.print_build_summary()

if __name__ == "__main__":
    main()