# BatchWatermark - 批量图片水印桌面应用 🚀

一个功能强大的桌面应用程序，专为批量图片水印处理和Excel报告自动生成而设计。基于Python和Tkinter构建，具有智能分组检测、可定制水印和综合项目文档等特性。

## 📋 目录

- [🎯 项目概述](#-项目概述)
- [✨ 功能特性](#-功能特性)
- [🚀 快速开始](#-快速开始)
- [🔧 技术栈](#-技术栈)
- [🏗️ 项目结构](#️-项目结构)
- [⚙️ 安装配置](#️-安装配置)
- [🛠️ 开发指南](#️-开发指南)
- [📦 应用构建](#-应用构建)
- [🧪 测试指南](#-测试指南)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)

## 🎯 项目概述

BatchWatermark是一个跨平台桌面应用程序，专为专业图像处理工作流程设计。它能够自动检测图像文件夹，应用可定制的水印（包含项目信息和时间戳），并生成全面的Excel报告。

### 核心能力
- **智能分组检测**: 自动扫描目录结构并识别图像文件夹
- **批量水印处理**: 使用可定制水印模板处理多个图像组
- **Excel报告生成**: 创建包含嵌入式处理图像的详细报告
- **实时进度监控**: 可视化进度指示器和详细日志记录
- **跨平台支持**: 在Windows、macOS和Linux上运行

## ✨ 功能特性

### 🔍 智能文件夹检测
- 自动发现目录结构中的图像文件夹
- 过滤系统文件夹和无关目录
- 支持多种图像格式（JPG、PNG、GIF、BMP、WEBP）
- 基于检测内容的动态配置

### 🎨 高级水印处理
- **项目信息**: 可定制的项目名称、区域和内容字段
- **组别标识**: 自动组名标记
- **日期标记**: 带有可配置起始日期的连续日期水印
- **专业布局**: 圆角、渐变背景和优化的排版
- **高质量输出**: 在添加清晰水印的同时保持图像质量

### 📊 Excel报告生成
- **多工作表报告**: 每个图像组单独的Excel工作表
- **嵌入式图像**: 直接图像嵌入和自动调整大小
- **专业格式**: 标准化布局和适当的间距
- **批量导出**: 一键生成综合报告

### 🎛️ 灵活配置
- **项目设置**: 可定制的项目信息和水印内容
- **组管理**: 日期、计数和输出文件夹的单独组配置
- **批量操作**: 多个组的批量配置更新
- **实时预览**: 配置更改的即时应用

### 🔄 用户体验
- **进度跟踪**: 实时进度条和状态更新
- **中断控制**: 安全的开始/停止处理和优雅关闭
- **详细日志**: 带时间戳的全面操作日志
- **错误处理**: 用户友好的错误消息和恢复建议

## 🚀 快速开始

### 开发者

1. **克隆仓库**
   ```bash
   git clone <仓库URL>
   cd BatchWatermark
   ```

2. **设置环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. **运行开发版本**
   ```bash
   python batch_watermark.py
   ```

### 最终用户

详细的安装和使用说明请参见[USER_GUIDE_CN.md](USER_GUIDE_CN.md)。

## 🔧 技术栈

### 核心技术
- **Python 3.8+** - 主要开发语言
- **Tkinter** - 跨平台GUI框架
- **Pillow (PIL)** - 高级图像处理功能
- **OpenPyXL** - Excel文件操作和图像嵌入
- **PyInstaller** - 应用程序打包和分发

### 架构组件
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GUI层         │    │  业务逻辑层      │    │   数据层        │
│                 │    │                  │    │                 │
│ BatchWatermarkGUI│◄──►│ WatermarkProcessor│◄──►│ 文件系统        │
│ Tkinter界面     │    │ 图像处理         │    │ 图像文件        │
│ 事件处理        │    │ Excel生成        │    │ 配置数据        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 依赖项
```
Pillow>=10.0.0      # 图像处理和格式支持
openpyxl>=3.1.0     # Excel文件操作和图像嵌入
pyinstaller>=6.0.0  # 应用程序打包分发
```

## 🏗️ 项目结构

```
BatchWatermark/
├── batch_watermark.py      # 主应用程序文件
├── requirements.txt        # Python依赖项
├── README.md              # 英文开发者文档
├── README_CN.md           # 中文开发者文档
├── USER_GUIDE.md          # 英文用户手册
├── USER_GUIDE_CN.md       # 中文用户手册
├── app_icon_design.html   # 图标设计模板
├── assets/                # 应用程序资源
│   ├── app_icon.ico       # Windows应用程序图标
│   ├── app_icon.icns      # macOS应用程序图标
│   └── screenshots/       # 应用程序截图
├── scripts/               # 构建和实用脚本
│   └── build.py          # 自动化构建脚本
├── dist/                  # 构建应用程序输出
├── build/                 # 临时构建文件
└── .github/              # GitHub Actions工作流
    └── workflows/
        └── build.yml     # 自动化构建管道
```

## ⚙️ 安装配置

### 先决条件
- Python 3.8或更高版本
- pip包管理器
- Git（用于开发）

### 开发环境设置

1. **安装Python依赖项**
   ```bash
   pip install -r requirements.txt
   ```

2. **验证安装**
   ```bash
   python batch_watermark.py
   ```

3. **运行测试**（如果可用）
   ```bash
   python -m pytest tests/
   ```

## 🛠️ 开发指南

### 核心组件

#### BatchWatermarkGUI类
- **用途**: 管理图形用户界面和用户交互
- **关键方法**:
  - `scan_groups_from_directory()`: 智能文件夹检测和分析
  - `configure_project()`: 项目信息管理界面
  - `toggle_processing()`: 处理控制和状态管理

#### WatermarkProcessor类
- **用途**: 处理图像处理和业务逻辑操作
- **关键方法**:
  - `process_single_group()`: 单个图像组的完整工作流程
  - `add_date_watermark()`: 带有自定义布局的高级水印应用
  - `generate_excel_report()`: 全面的Excel报告创建

### 代码规范指南

#### 命名约定
- **类**: PascalCase（例如：`BatchWatermarkGUI`）
- **方法**: snake_case（例如：`process_single_group`）
- **常量**: UPPER_SNAKE_CASE（例如：`DEFAULT_GROUP_TEMPLATE`）

#### 文档标准
```python
def add_date_watermark(self, image_path, output_path, date_str, group_name):
    \"\"\"为图像应用包含项目信息的日期水印。
    
    参数:
        image_path (str): 输入图像文件路径
        output_path (str): 输出图像文件路径
        date_str (str): YYYYMMDD格式的日期字符串
        group_name (str): 水印的组标识符
    
    返回:
        bool: 如果水印应用成功则为True
        
    异常:
        PIL.UnidentifiedImageError: 如果图像格式不受支持
        IOError: 如果文件操作失败
    \"\"\"
```

### 添加新功能

#### 水印自定义
1. 修改`WatermarkProcessor`中的`add_date_watermark()`方法
2. 更新`BatchWatermarkGUI.__init__()`中的`watermark_config`字典
3. 在`configure_project()`中添加配置UI元素

#### 图像格式支持
1. 更新`PROCESS_CONFIG["支持格式"]`列表
2. 测试与PIL的格式兼容性
3. 更新文档

#### 导出格式扩展
1. 参考`generate_excel_report()`实现
2. 创建新的导出方法（例如：`generate_pdf_report()`）
3. 添加格式选择的UI控件

## 📦 应用构建

### 基本构建
```bash
# 推荐：目录模式，兼容性更好
pyinstaller --onedir --windowed --name="BatchWatermark" batch_watermark.py

# 替代方案：单文件模式，分发体积更小
pyinstaller --onefile --windowed --name="BatchWatermark" batch_watermark.py
```

### 高级构建配置
```bash
# 带自定义图标
pyinstaller --onedir --windowed --icon=assets/app_icon.ico --name="BatchWatermark" batch_watermark.py

# 排除不必要的模块以减小体积
pyinstaller --onedir --windowed --exclude-module=matplotlib --name="BatchWatermark" batch_watermark.py
```

### 构建脚本
```python
# scripts/build.py
import subprocess
import sys

def build_application():
    \"\"\"BatchWatermark应用程序的自动化构建脚本。\"\"\"
    build_command = [
        \"pyinstaller\",
        \"--onedir\",
        \"--windowed\",
        \"--icon=assets/app_icon.ico\",
        \"--name=BatchWatermark\",
        \"batch_watermark.py\"
    ]
    
    try:
        subprocess.run(build_command, check=True)
        print(\"✅ 构建成功完成!\")
    except subprocess.CalledProcessError as e:
        print(f\"❌ 构建失败: {e}\")
        sys.exit(1)

if __name__ == \"__main__\":
    build_application()
```

### 跨平台注意事项
- **Windows**: 使用`.ico`图标格式
- **macOS**: 使用`.icns`图标格式
- **Linux**: 标准PNG图标效果良好

## 🧪 测试指南

### 单元测试
```python
import unittest
from batch_watermark import WatermarkProcessor, BatchWatermarkGUI

class TestWatermarkProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = WatermarkProcessor(test_dir, mock_gui, test_config)
    
    def test_watermark_generation(self):
        result = self.processor.add_date_watermark(
            \"test_input.jpg\", 
            \"test_output.jpg\", 
            \"20250601\", 
            \"测试组\"
        )
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
```

### 集成测试
1. 准备包含示例图像的测试目录结构
2. 运行完整的处理工作流程
3. 验证输出质量和报告准确性
4. 测试无效输入的错误处理

### 性能测试
- 测量不同图像计数的处理时间
- 监控大批量操作期间的内存使用情况
- 测试处理期间的UI响应性

## 🤝 贡献指南

我们欢迎对BatchWatermark的贡献！请遵循以下指南：

### 入门指南
1. Fork仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 进行更改
4. 为新功能编写测试
5. 确保所有测试通过
6. 提交更改（`git commit -m '添加惊人功能'`）
7. 推送到你的分支（`git push origin feature/amazing-feature`）
8. 打开Pull Request

### 代码审查流程
- 所有更改在合并前都需要审查
- 确保代码遵循样式指南
- 包含适当的文档更新
- 为新功能添加测试

### 错误报告
报告错误时，请包含：
- 操作系统和版本
- Python版本
- 重现问题的步骤
- 预期与实际行为
- 如果适用，请提供截图

## 📄 许可证

本项目采用MIT许可证 - 详情请参见[LICENSE](LICENSE)文件。

## 🙏 致谢

- **PIL/Pillow团队** - 出色的图像处理功能
- **OpenPyXL开发者** - 强大的Excel文件操作
- **Python社区** - 杰出的生态系统和支持

## 📞 支持

- **文档**: 使用说明请参见[USER_GUIDE_CN.md](USER_GUIDE_CN.md)
- **问题**: 通过GitHub Issues报告错误和功能请求
- **讨论**: 加入社区讨论进行问题和想法交流

---

**用❤️为开发者社区开发**  
**最后更新**: 2025-07-01  
**版本**: 1.0.0