# BatchWatermark User Guide 📚

Welcome to BatchWatermark! This comprehensive guide will help you get started with the batch image watermarking application quickly and effectively.

## 📋 Table of Contents

- [🎯 What is BatchWatermark?](#-what-is-batchwatermark)
- [⚡ Quick Start](#-quick-start)
- [📥 Installation](#-installation)
- [📁 Preparing Your Images](#-preparing-your-images)
- [🎮 Using the Application](#-using-the-application)
- [⚙️ Configuration](#️-configuration)
- [📊 Understanding Results](#-understanding-results)
- [💡 Tips and Best Practices](#-tips-and-best-practices)
- [❓ Troubleshooting](#-troubleshooting)
- [📞 Getting Help](#-getting-help)

## 🎯 What is BatchWatermark?

BatchWatermark is a user-friendly desktop application that helps you:

- **Process multiple images at once** - Save time by handling hundreds of images automatically
- **Add professional watermarks** - Include project information, dates, and group identifiers
- **Generate Excel reports** - Create comprehensive documentation with all processed images
- **Organize your workflow** - Automatically detect and process image groups

### Perfect for:
- Project managers documenting work progress
- Construction teams organizing daily reports
- Photographers adding consistent branding
- Any professional needing batch image processing

## ⚡ Quick Start

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux Ubuntu 18.04+
- **Memory**: 4GB RAM minimum (8GB recommended for large batches)
- **Storage**: 1GB free space plus space for your images
- **Display**: 1280x720 resolution minimum

### 5-Minute Setup
1. **Download** BatchWatermark from the releases page
2. **Extract** the application to your preferred location
3. **Double-click** the application icon to launch
4. **Select** your image folder
5. **Click** "Start Processing" and you're done!

## 📥 Installation

### Windows
1. Download `BatchWatermark-Windows.zip`
2. Extract to `C:\\Program Files\\BatchWatermark\\` (or your preferred location)
3. Double-click `BatchWatermark.exe` to run
4. If Windows shows a security warning, click "More info" → "Run anyway"

### macOS
1. Download `BatchWatermark-macOS.dmg`
2. Open the DMG file and drag BatchWatermark to Applications
3. Right-click the app and select "Open" (first time only)
4. Click "Open" in the security dialog

### Linux
1. Download `BatchWatermark-Linux.tar.gz`
2. Extract: `tar -xzf BatchWatermark-Linux.tar.gz`
3. Make executable: `chmod +x BatchWatermark/BatchWatermark`
4. Run: `./BatchWatermark/BatchWatermark`

## 📁 Preparing Your Images

### Folder Structure
Organize your images like this:
```
Your Project Folder/
├── Group1/              # e.g., "Construction Team"
│   ├── image1.jpg
│   ├── image2.png
│   └── image3.jpg
├── Group2/              # e.g., "Quality Control"
│   ├── photo1.jpg
│   └── photo2.png
└── Group3/              # e.g., "Safety Team"
    ├── pic1.jpg
    └── pic2.jpg
```

### Supported Image Formats
- **JPEG** (.jpg, .jpeg) - Most common format
- **PNG** (.png) - High quality with transparency support
- **GIF** (.gif) - Animated images (processed as static)
- **BMP** (.bmp) - Windows bitmap format
- **WEBP** (.webp) - Modern web format

### Image Requirements
- **Minimum size**: 800x600 pixels
- **Recommended size**: 1920x1080 pixels or higher
- **File naming**: Any name (app will rename automatically)
- **File size**: No specific limit (larger files take longer to process)

## 🎮 Using the Application

### Step 1: Launch the Application
- Double-click the BatchWatermark icon
- Wait for the application window to appear
- You'll see the main interface with several buttons and options

### Step 2: Select Your Working Directory
1. Click the **"Browse"** button
2. Navigate to your main project folder (the one containing all group folders)
3. Select the folder and click "Select Folder"
4. The app will automatically scan and detect image groups

### Step 3: Review Detected Groups
- A dialog will show all detected groups
- Check that all your image folders are listed
- Note the image count for each group
- Click **"Confirm"** to proceed

### Step 4: Configure Project Information (Optional)
1. Click **"🏷️ Project Settings"** button
2. Enter your project details:
   - **Project Name**: Your project title
   - **Work Area**: Location or area description
   - **Work Content**: Type of work being documented
3. Click **"💾 Save"** to apply changes

### Step 5: Adjust Group Settings (Optional)
1. Click **"⚙️ Configure Groups"** button
2. For each group, you can modify:
   - **Processing Month**: Set the month for date watermarks
   - **Number of Days**: How many days to process
   - **Start Date**: When the date sequence should begin
   - **Output Folder**: Custom name for the result folder
3. Use **"Batch Set Month"** to quickly configure all groups
4. Click **"✅ Done"** when finished

### Step 6: Start Processing
1. Click the **"🎯 Start Processing"** button
2. Watch the progress bar and status messages
3. The application will:
   - Rename and resize images
   - Add watermarks with project information
   - Generate an Excel report
4. You can click **"⏹️ Stop Processing"** if needed

### Step 7: View Results
1. When processing completes, click **"📁 Open Results"**
2. Your results are organized in the "Watermarked" folder:
   - Individual group folders with processed images
   - "Image Collection.xlsx" with all images in spreadsheet format

## ⚙️ Configuration

### Project Settings
Access via **"🏷️ Project Settings"** button:

- **Project Name**: Appears prominently on watermarks
- **Work Area**: Describes the location or site
- **Work Content**: Type of activity being documented

### Group Configuration
Access via **"⚙️ Configure Groups"** button:

#### Batch Operations
- **Batch Set Month**: Quickly set the same month/year for all groups
- **Rescan**: Refresh the group detection if you added new folders

#### Individual Group Settings
- **Group Name**: Display name for watermarks
- **Processing Month**: Month/year for the image sequence
- **Processing Days**: Number of images to process
- **Start Date**: First date in the sequence
- **Output Number**: Folder name for results

### Advanced Tips
- **Date Sequences**: Images get sequential dates starting from your chosen start date
- **Image Shuffling**: Original order is randomized for variety
- **Quality Settings**: Images are optimized for quality while reducing file size

## 📊 Understanding Results

### Output Structure
After processing, you'll find:
```
Watermarked/
├── Group1/              # Processed images for first group
│   ├── watermarked_image001.png
│   ├── watermarked_image002.png
│   └── ...
├── Group2/              # Processed images for second group
│   └── ...
└── Image Collection.xlsx # Excel report with all images
```

### Watermark Information
Each image includes:
- **Project Name** (prominent header)
- **Work Area**: Your specified location
- **Work Content**: Type of work
- **Work Group**: Group/team name
- **Photo Date**: Sequential dates from your start date

### Excel Report Features
- **Multiple Worksheets**: One tab per group
- **Embedded Images**: Full-size images displayed in cells
- **Professional Layout**: Organized for easy viewing and printing
- **Scalable Images**: Automatically sized for optimal display

## 💡 Tips and Best Practices

### Organizing Images
- **Use descriptive folder names** - They become group names in watermarks
- **Keep similar image counts per group** - For consistent reporting
- **Remove unwanted images first** - Clean up before processing

### Optimizing Performance
- **Close other applications** - Free up memory for processing
- **Process in smaller batches** - If you have thousands of images
- **Use SSD storage** - Faster disk access improves speed

### Quality Results
- **Use high-resolution source images** - Better watermark clarity
- **Check date sequences** - Ensure start dates make sense
- **Preview configuration** - Use the group configuration dialog to verify settings

### Workflow Efficiency
- **Set up templates** - Configure project settings once, reuse for similar projects
- **Use batch operations** - Configure multiple groups at once
- **Monitor progress** - Watch the log for any issues during processing

### File Management
- **Backup originals** - Keep copies of your source images
- **Organize outputs** - Use descriptive output folder names
- **Archive completed projects** - Move finished work to long-term storage

## ❓ Troubleshooting

### Application Won't Start
**Problem**: Double-clicking does nothing or shows error

**Solutions**:
- **Windows**: Right-click → "Run as administrator"
- **macOS**: Right-click → "Open" (bypass security warning)
- **Linux**: Check file permissions: `chmod +x BatchWatermark`
- **All systems**: Try moving app to a folder without spaces in the path

### No Groups Detected
**Problem**: "No image groups found" message appears

**Solutions**:
- Ensure each folder contains at least one image file
- Check that image files have supported extensions (.jpg, .png, etc.)
- Avoid special characters in folder names
- Make sure you selected the parent folder, not an image folder

### Processing Errors
**Problem**: Some images fail to process

**Solutions**:
- Check that all image files can be opened in other applications
- Ensure sufficient free disk space (at least 2x your image folder size)
- Close other memory-intensive applications
- Try processing smaller groups if you have many large images

### Excel File Won't Open
**Problem**: Generated Excel file shows errors

**Solutions**:
- Install Microsoft Office or LibreOffice
- Check if file is being used by another program
- Try copying the file to a different location
- Ensure you have enough free disk space

### Watermarks Look Wrong
**Problem**: Text is cut off or poorly positioned

**Solutions**:
- Use larger source images (minimum 1920x1080)
- Keep project names reasonably short
- Check that system fonts are installed properly
- Try running as administrator (Windows) or with elevated permissions

### Slow Performance
**Problem**: Processing takes very long

**Solutions**:
- Close unnecessary applications to free memory
- Move images to faster storage (SSD vs HDD)
- Process fewer images at once
- Reduce source image resolution if possible

### Memory Issues
**Problem**: "Out of memory" errors

**Solutions**:
- Process groups separately instead of all at once
- Restart the application between large batches
- Increase virtual memory (swap file) on your system
- Consider upgrading system RAM for large projects

## 📞 Getting Help

### Documentation
- **This Guide**: Complete user instructions
- **Developer Documentation**: [README.md](README.md) for technical details
- **Chinese Version**: [USER_GUIDE_CN.md](USER_GUIDE_CN.md) for Chinese users

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share tips with other users
- **Documentation Updates**: Suggest improvements to this guide

### Technical Information
When seeking help, please provide:
- **Operating System**: Version and type (Windows 10, macOS 12, Ubuntu 20.04, etc.)
- **Application Version**: Check the About dialog
- **Error Messages**: Exact text of any error messages
- **Steps to Reproduce**: What you were doing when the problem occurred
- **Sample Data**: If possible, a small sample of your images and folder structure

### Before Reporting Issues
1. **Check this guide** - Look for your issue in the troubleshooting section
2. **Try restarting** - Close and reopen the application
3. **Test with simple data** - Try a few images in a simple folder structure
4. **Check system requirements** - Ensure your system meets minimum requirements

---

**Thank you for using BatchWatermark!** 

We hope this guide helps you create professional watermarked images efficiently. If you have suggestions for improving this documentation, please let us know.

**Last Updated**: 2025-07-01  
**Version**: 1.0.0