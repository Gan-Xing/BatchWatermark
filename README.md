# BatchWatermark - Batch Image Watermarking Desktop Application 🚀

A powerful desktop application for batch image watermarking with automatic Excel report generation. Built with Python and Tkinter, featuring intelligent group detection, customizable watermarks, and comprehensive project documentation.

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🔧 Technology Stack](#-technology-stack)
- [🏗️ Project Structure](#️-project-structure)
- [⚙️ Installation](#️-installation)
- [🛠️ Development](#️-development)
- [📦 Building](#-building)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 Overview

BatchWatermark is a cross-platform desktop application designed for professional image processing workflows. It automatically detects image folders, applies customizable watermarks with project information and timestamps, and generates comprehensive Excel reports.

### Key Capabilities
- **Intelligent Group Detection**: Automatically scans directory structures and identifies image folders
- **Batch Watermarking**: Processes multiple image groups with customizable watermark templates
- **Excel Report Generation**: Creates detailed reports with embedded processed images
- **Real-time Progress Monitoring**: Visual progress indicators and detailed logging
- **Cross-platform Support**: Runs on Windows, macOS, and Linux

## ✨ Features

### 🔍 Smart Folder Detection
- Automatically discovers image folders in directory structures
- Filters out system folders and irrelevant directories
- Supports multiple image formats (JPG, PNG, GIF, BMP, WEBP)
- Dynamic configuration based on detected content

### 🎨 Advanced Watermarking
- **Project Information**: Customizable project name, area, and content fields
- **Group Identification**: Automatic group name labeling
- **Date Stamping**: Sequential date watermarks with configurable start dates
- **Professional Layout**: Rounded corners, gradient backgrounds, and optimized typography
- **High Quality Output**: Maintains image quality while adding clear watermarks

### 📊 Excel Report Generation
- **Multi-sheet Reports**: Separate Excel worksheets for each image group
- **Embedded Images**: Direct image embedding with automatic sizing
- **Professional Formatting**: Standardized layout with proper spacing
- **Batch Export**: Single-click generation of comprehensive reports

### 🎛️ Flexible Configuration
- **Project Settings**: Customizable project information and watermark content
- **Group Management**: Individual group configuration for dates, counts, and output folders
- **Batch Operations**: Mass configuration updates for multiple groups
- **Real-time Preview**: Immediate application of configuration changes

### 🔄 User Experience
- **Progress Tracking**: Real-time progress bars and status updates
- **Interrupt Control**: Safe start/stop processing with graceful shutdown
- **Detailed Logging**: Comprehensive operation logs with timestamps
- **Error Handling**: User-friendly error messages and recovery suggestions

## 🚀 Quick Start

### For Developers

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd BatchWatermark
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. **Run Development Version**
   ```bash
   python batch_watermark.py
   ```

### For End Users

See [USER_GUIDE.md](USER_GUIDE.md) for detailed installation and usage instructions.

## 🔧 Technology Stack

### Core Technologies
- **Python 3.8+** - Primary development language
- **Tkinter** - Cross-platform GUI framework
- **Pillow (PIL)** - Advanced image processing capabilities
- **OpenPyXL** - Excel file manipulation and image embedding
- **PyInstaller** - Application packaging and distribution

### Architecture Components
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GUI Layer     │    │  Business Logic  │    │   Data Layer    │
│                 │    │                  │    │                 │
│ BatchWatermarkGUI│◄──►│ WatermarkProcessor│◄──►│ File System     │
│ Tkinter Interface│    │ Image Processing │    │ Image Files     │
│ Event Handling  │    │ Excel Generation │    │ Configuration   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Dependencies
```
Pillow>=10.0.0      # Image processing and format support
openpyxl>=3.1.0     # Excel file operations with image embedding
pyinstaller>=6.0.0  # Application packaging for distribution
```

## 🏗️ Project Structure

```
BatchWatermark/
├── batch_watermark.py      # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # English developer documentation
├── README_CN.md           # Chinese developer documentation
├── USER_GUIDE.md          # English user manual
├── USER_GUIDE_CN.md       # Chinese user manual
├── app_icon_design.html   # Icon design templates
├── assets/                # Application assets
│   ├── app_icon.ico       # Windows application icon
│   ├── app_icon.icns      # macOS application icon
│   └── screenshots/       # Application screenshots
├── scripts/               # Build and utility scripts
│   └── build.py          # Automated build script
├── dist/                  # Built application outputs
├── build/                 # Temporary build files
└── .github/              # GitHub Actions workflows
    └── workflows/
        └── build.yml     # Automated build pipeline
```

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for development)

### Development Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python batch_watermark.py
   ```

3. **Run Tests** (if available)
   ```bash
   python -m pytest tests/
   ```

## 🛠️ Development

### Core Components

#### BatchWatermarkGUI Class
- **Purpose**: Manages the graphical user interface and user interactions
- **Key Methods**:
  - `scan_groups_from_directory()`: Intelligent folder detection and analysis
  - `configure_project()`: Project information management interface
  - `toggle_processing()`: Process control and state management

#### WatermarkProcessor Class
- **Purpose**: Handles image processing and business logic operations
- **Key Methods**:
  - `process_single_group()`: Complete workflow for individual image groups
  - `add_date_watermark()`: Advanced watermark application with custom layouts
  - `generate_excel_report()`: Comprehensive Excel report creation

### Code Style Guidelines

#### Naming Conventions
- **Classes**: PascalCase (e.g., `BatchWatermarkGUI`)
- **Methods**: snake_case (e.g., `process_single_group`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_GROUP_TEMPLATE`)

#### Documentation Standards
```python
def add_date_watermark(self, image_path, output_path, date_str, group_name):
    \"\"\"Apply date watermark to image with project information.
    
    Args:
        image_path (str): Input image file path
        output_path (str): Output image file path
        date_str (str): Date string in YYYYMMDD format
        group_name (str): Group identifier for watermark
    
    Returns:
        bool: True if watermark application successful
        
    Raises:
        PIL.UnidentifiedImageError: If image format is unsupported
        IOError: If file operations fail
    \"\"\"
```

### Adding New Features

#### Watermark Customization
1. Modify the `add_date_watermark()` method in `WatermarkProcessor`
2. Update `watermark_config` dictionary in `BatchWatermarkGUI.__init__()`
3. Add configuration UI elements in `configure_project()`

#### Image Format Support
1. Update `PROCESS_CONFIG["支持格式"]` list
2. Test format compatibility with PIL
3. Update documentation

#### Export Format Extensions
1. Reference `generate_excel_report()` implementation
2. Create new export methods (e.g., `generate_pdf_report()`)
3. Add UI controls for format selection

## 📦 Building

### 🚀 Automated Build (Recommended)

The easiest way to build BatchWatermark is using our automated build script:

```bash
# Run the automated build script
python scripts/build.py
```

**Features of the automated build script:**
- 🔍 **Smart Dependency Detection**: Automatically checks for required dependencies
- 🎨 **Intelligent Icon Handling**: Detects and converts icons to appropriate formats (ICO/ICNS)
- 🌍 **Cross-Platform Support**: Builds native applications for Windows, macOS, and Linux
- 📦 **Distribution Package**: Creates complete distribution packages with documentation
- ✅ **Error Handling**: Provides clear error messages and recovery suggestions

**Build Script Options:**
```bash
# Basic build
python scripts/build.py

# Clean build (removes previous build files)
python scripts/build.py --clean

# Build with custom output directory
python scripts/build.py --output-dir /path/to/output
```

### Manual Build Commands

If you prefer manual control or need to customize the build process:

#### Basic Build
```bash
# Recommended: Directory mode for better compatibility
pyinstaller --onedir --windowed --name="BatchWatermark" batch_watermark.py

# Alternative: Single file mode for smaller distribution
pyinstaller --onefile --windowed --name="BatchWatermark" batch_watermark.py
```

#### Advanced Build Configuration
```bash
# With custom icon
pyinstaller --onedir --windowed --icon=assets/app_icon.ico --name="BatchWatermark" batch_watermark.py

# Excluding unnecessary modules for smaller size
pyinstaller --onedir --windowed --exclude-module=matplotlib --name="BatchWatermark" batch_watermark.py
```

### Cross-Platform Considerations
- **Windows**: Use `.ico` icon format
- **macOS**: Use `.icns` icon format  
- **Linux**: Standard PNG icons work well

## 🧪 Testing

### Unit Testing
```python
import unittest
from batch_watermark import WatermarkProcessor, BatchWatermarkGUI

class TestWatermarkProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = WatermarkProcessor(test_dir, mock_gui, test_config)
    
    def test_watermark_generation(self):
        result = self.processor.add_date_watermark(
            "test_input.jpg", 
            "test_output.jpg", 
            "20250601", 
            "Test Group"
        )
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing
1. Prepare test directory structure with sample images
2. Run complete processing workflow
3. Verify output quality and report accuracy
4. Test error handling with invalid inputs

### Performance Testing
- Measure processing time for different image counts
- Monitor memory usage during large batch operations
- Test UI responsiveness during processing

## 🤝 Contributing

We welcome contributions to BatchWatermark! Please follow these guidelines:

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Review Process
- All changes require review before merging
- Ensure code follows style guidelines
- Include appropriate documentation updates
- Add tests for new features

### Bug Reports
When reporting bugs, please include:
- Operating system and version
- Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PIL/Pillow Team** - Excellent image processing capabilities
- **OpenPyXL Developers** - Robust Excel file manipulation
- **Python Community** - Outstanding ecosystem and support

## 📞 Support

- **Documentation**: See [USER_GUIDE.md](USER_GUIDE.md) for usage instructions
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions for questions and ideas

---

**Developed with ❤️ for the developer community**  
**Last Updated**: 2025-07-01  
**Version**: 1.0.0
