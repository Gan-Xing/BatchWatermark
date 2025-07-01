#!/usr/bin/env python3
"""
邦杜库项目图片处理GUI版本
整合所有功能到单个文件，提供友好的图形界面
"""

import os
import sys
import shutil
import re
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFile
import threading

ImageFile.LOAD_TRUNCATED_IMAGES = True

# 配置信息 - 内嵌到文件中
GROUPS_CONFIG = {
    "土方组": {
        "folder": "土方组",
        "output_folder": "1",
        "班组名称": "土方组",
        "月份": "2025-06",
        "天数": 30,
        "起始日期": "2025-06-01"
    },
    "场站组": {
        "folder": "场站组", 
        "output_folder": "2",
        "班组名称": "场站组",
        "月份": "2025-06",
        "天数": 30,
        "起始日期": "2025-06-01"
    },
    "实验室": {
        "folder": "实验室",
        "output_folder": "3", 
        "班组名称": "实验室",
        "月份": "2025-06",
        "天数": 30,
        "起始日期": "2025-06-01"
    },
    "结构组": {
        "folder": "结构组",
        "output_folder": "4",
        "班组名称": "结构组", 
        "月份": "2025-06",
        "天数": 30,
        "起始日期": "2025-06-01"
    }
}

WATERMARK_CONFIG = {
    "项目名称": "科特迪瓦邦杜库边境路",
    "施工区域": "项目营地",
    "施工内容": "每日班前教育",
    "字体大小": 36,
    "背景色": (100, 149, 237, 200),
    "文字颜色": (255, 255, 255, 255)
}

PROCESS_CONFIG = {
    "目标宽度": 1920,
    "目标高度": 1080,
    "支持格式": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    "输出质量": 95
}

PATHS = {
    "输入目录": "input_images",
    "输出目录": "output_images", 
    "水印后目录": "水印后",
    "主脚本": "script.py"
}

class BandukuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("邦杜库项目图片处理系统")
        self.root.geometry("800x600")
        
        # 工作目录设置
        self.base_dir = None
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="🚀 邦杜库项目图片处理自动化系统", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 工作目录选择
        dir_frame = ttk.LabelFrame(main_frame, text="工作目录设置", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.dir_var = tk.StringVar()
        ttk.Label(dir_frame, text="选择包含班组文件夹的根目录:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(dir_frame, textvariable=self.dir_var, width=60).grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(dir_frame, text="浏览", command=self.browse_directory).grid(row=1, column=1)
        
        dir_frame.columnconfigure(0, weight=1)
        
        # 控制按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="🎯 开始处理", command=self.start_processing)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="⚙️ 配置班组", command=self.configure_groups).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📁 打开结果", command=self.open_results).pack(side=tk.LEFT)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # 状态标签
        self.status_var = tk.StringVar(value="准备就绪")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=2)
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="处理日志", padding="5")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        log_msg = f"[{timestamp}] {symbols.get(level, 'ℹ️')} {message}\n"
        
        self.log_text.insert(tk.END, log_msg)
        self.log_text.see(tk.END)
        self.root.update()
        
    def browse_directory(self):
        directory = filedialog.askdirectory(title="选择包含班组文件夹的根目录")
        if directory:
            self.dir_var.set(directory)
            self.base_dir = Path(directory)
            self.log(f"已选择工作目录: {directory}")
            
    def configure_groups(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("班组配置")
        config_window.geometry("600x400")
        config_window.grab_set()
        
        # 创建配置界面
        frame = ttk.Frame(config_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="班组配置", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # 配置表格
        tree = ttk.Treeview(frame, columns=("班组", "月份", "天数", "起始日期"), show="headings", height=8)
        tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 列标题
        tree.heading("班组", text="班组名称")
        tree.heading("月份", text="处理月份") 
        tree.heading("天数", text="天数")
        tree.heading("起始日期", text="起始日期")
        
        # 填充数据
        for group_key, config in GROUPS_CONFIG.items():
            tree.insert("", tk.END, values=(
                config["班组名称"], config["月份"], config["天数"], config["起始日期"]
            ))
        
        # 按钮框架
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        def update_all_config():
            year = simpledialog.askinteger("设置年份", "请输入年份 (如2025):", initialvalue=2025)
            if not year:
                return
            month = simpledialog.askinteger("设置月份", "请输入月份 (1-12):", initialvalue=6)
            if not month or not (1 <= month <= 12):
                messagebox.showerror("错误", "月份必须在1-12之间")
                return
                
            # 计算天数
            import calendar
            days = calendar.monthrange(year, month)[1]
            
            # 更新所有配置
            for group_config in GROUPS_CONFIG.values():
                group_config["月份"] = f"{year:04d}-{month:02d}"
                group_config["天数"] = days
                group_config["起始日期"] = f"{year:04d}-{month:02d}-01"
            
            # 刷新表格
            for item in tree.get_children():
                tree.delete(item)
            for group_key, config in GROUPS_CONFIG.items():
                tree.insert("", tk.END, values=(
                    config["班组名称"], config["月份"], config["天数"], config["起始日期"]
                ))
                
            messagebox.showinfo("成功", f"已更新所有班组配置为 {year}年{month}月")
        
        ttk.Button(btn_frame, text="批量设置月份", command=update_all_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="关闭", command=config_window.destroy).pack(side=tk.RIGHT)
        
    def open_results(self):
        if not self.base_dir:
            messagebox.showwarning("警告", "请先选择工作目录")
            return
            
        result_dir = self.base_dir / "水印后"
        if result_dir.exists():
            if sys.platform == "win32":
                os.startfile(result_dir)
            elif sys.platform == "darwin":
                subprocess.run(["open", result_dir])
            else:
                subprocess.run(["xdg-open", result_dir])
        else:
            messagebox.showinfo("提示", "结果目录不存在，请先进行处理")
            
    def start_processing(self):
        if not self.base_dir:
            messagebox.showwarning("警告", "请先选择工作目录")
            return
            
        if self.is_processing:
            messagebox.showinfo("提示", "正在处理中，请等待完成")
            return
            
        # 在新线程中运行处理
        self.is_processing = True
        self.start_btn.config(state="disabled")
        thread = threading.Thread(target=self.run_processing, daemon=True)
        thread.start()
        
    def run_processing(self):
        try:
            processor = BandukuProcessor(self.base_dir, self)
            success = processor.run_full_process()
            
            if success:
                self.log("🎉 所有班组处理完成!", "SUCCESS")
                messagebox.showinfo("完成", "所有班组处理完成!")
            else:
                self.log("⚠️ 部分班组处理失败", "WARNING")
                messagebox.showwarning("警告", "部分班组处理失败，请查看日志")
                
        except Exception as e:
            self.log(f"处理异常: {str(e)}", "ERROR")
            messagebox.showerror("错误", f"处理过程中出现错误:\n{str(e)}")
        finally:
            self.is_processing = False
            self.start_btn.config(state="normal")
            self.status_var.set("处理完成")
            self.progress_var.set(0)

class BandukuProcessor:
    def __init__(self, base_dir, gui):
        self.base_dir = Path(base_dir)
        self.gui = gui
        self.input_dir = self.base_dir / PATHS["输入目录"]
        self.output_dir = self.base_dir / PATHS["输出目录"]
        self.watermark_dir = self.base_dir / PATHS["水印后目录"]
        
        # 确保目录存在
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.watermark_dir.mkdir(exist_ok=True)
        
        self.gui.log("🚀 邦杜库项目图片处理系统启动")
        self.gui.log(f"📁 工作目录: {self.base_dir}")
        self.gui.log(f"📊 配置班组数量: {len(GROUPS_CONFIG)}")

    def run_shell_command(self, command, cwd=None):
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd or self.base_dir,
                capture_output=True, 
                text=True, 
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            self.gui.log(f"命令执行失败: {command}", "ERROR")
            self.gui.log(f"错误信息: {e.stderr}", "ERROR")
            return False, e.stderr

    def clear_directory(self, directory):
        if directory.exists():
            for item in directory.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            self.gui.log(f"已清空目录: {directory.name}")

    def count_images_in_directory(self, directory):
        if not directory.exists():
            return 0
        
        image_count = 0
        for ext in PROCESS_CONFIG["支持格式"]:
            image_count += len(list(directory.glob(f"*{ext}")))
            image_count += len(list(directory.glob(f"*{ext.upper()}")))
        return image_count

    def process_group_images(self, group_folder):
        group_path = self.base_dir / group_folder
        
        if not group_path.exists():
            self.gui.log(f"班组目录不存在: {group_folder}", "ERROR")
            return False

        self.gui.log(f"开始处理班组: {group_folder}")
        
        # 执行重命名脚本
        rename_script = group_path / "rename_images.py"
        if rename_script.exists():
            success, output = self.run_shell_command(f"python {rename_script}", cwd=group_path)
            if not success:
                self.gui.log("图片重命名失败", "ERROR")
                return False
        
        # 检查图片数量
        image_count = self.count_images_in_directory(group_path)
        self.gui.log(f"检测到图片数量: {image_count}")
        
        # 执行图片处理脚本
        resize_script = group_path / "resize_and_shuffle.sh"
        simple_script = group_path / "a.sh"
        
        if resize_script.exists():
            success, output = self.run_shell_command(f"bash {resize_script.name}", cwd=group_path)
            if not success and simple_script.exists():
                self.gui.log("尝试使用简化处理脚本...", "WARNING")
                success, output = self.run_shell_command(f"bash {simple_script.name}", cwd=group_path)
        elif simple_script.exists():
            success, output = self.run_shell_command(f"bash {simple_script.name}", cwd=group_path)
        else:
            self.gui.log("未找到图片处理脚本", "ERROR")
            return False
            
        if not success:
            self.gui.log("图片处理失败", "ERROR")
            return False
            
        self.gui.log(f"班组 {group_folder} 图片预处理完成", "SUCCESS")
        return True

    def copy_processed_images_to_input(self, group_folder):
        group_path = self.base_dir / group_folder
        
        # 清空input目录
        self.clear_directory(self.input_dir)
        
        # 复制图片到input目录
        copied_count = 0
        for ext in PROCESS_CONFIG["支持格式"]:
            for img_file in group_path.glob(f"*{ext}"):
                shutil.copy2(img_file, self.input_dir)
                copied_count += 1
            for img_file in group_path.glob(f"*{ext.upper()}"):
                shutil.copy2(img_file, self.input_dir)
                copied_count += 1
                
        self.gui.log(f"已复制 {copied_count} 张图片到输入目录")
        return copied_count

    def add_date_watermark(self, image_path, output_path, date_str, group_name):
        """添加日期水印到图片"""
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        
        # 尝试使用系统字体
        font_paths = [
            "/System/Library/Fonts/STHeiti Medium.ttc",  # macOS
            "C:/Windows/Fonts/simhei.ttf",  # Windows
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Linux
        ]
        
        font_size = 36
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
        
        if font is None:
            font = ImageFont.load_default()
            self.gui.log("警告：使用默认字体，中文可能显示异常", "WARNING")

        # 水印内容
        text_lines = [
            ("科特迪瓦邦杜库边境路", (100, 149, 237)),
            "施 工 区 域：项目营地",
            "施 工 内 容：每日班前教育",
            f"施 工 班 组：{group_name}",
            f"拍 摄 时 间：{datetime.strptime(date_str, '%Y%m%d').strftime('%Y.%m.%d')}"
        ]

        # 计算文字区域尺寸
        line_spacing = 16
        max_text_width = max(font.getlength(line[0] if isinstance(line, tuple) else line) for line in text_lines)
        total_height = (font_size + line_spacing) * len(text_lines)

        # 调整水印位置
        margin = 40
        x = margin
        y = height - total_height - margin

        # 创建背景层
        bg_layer = Image.new('RGBA', img.size, (255,255,255,0))
        bg_draw = ImageDraw.Draw(bg_layer)
        
        bg_width = max_text_width + 80
        extra_bottom_padding = 16
        total_height = (font_size + line_spacing) * len(text_lines) + extra_bottom_padding

        # 绘制白色背景
        bg_draw.rounded_rectangle(
            (x, y, x + bg_width, y + total_height),
            radius=8,
            fill=(255,255,255,128)
        )

        # 第一行蓝色背景
        first_line_height = font_size + 32
        first_line_y = y + (first_line_height - font_size) // 2

        bg_draw.rounded_rectangle(
            (x, y, x + bg_width, y + first_line_height),
            radius=8,
            fill=(100, 149, 237, 200)
        )

        # 合并图层
        img = Image.alpha_composite(img, bg_layer)
        draw = ImageDraw.Draw(img)

        # 绘制文字
        first_text = text_lines[0][0]
        first_text_width = font.getlength(first_text)
        first_text_x = x + (bg_width - first_text_width) // 2
        draw.text((first_text_x, first_line_y), first_text, font=font, fill=(255,255,255,255))

        # 绘制其余文字
        current_y = y + first_line_height + 8
        for line in text_lines[1:]:
            text = line[0] if isinstance(line, tuple) else line
            draw.text((x + 40, current_y), text, font=font, fill=(0,0,0,200))
            current_y += font_size + line_spacing

        # 保存图片
        img.convert('RGB').save(output_path, quality=95)

    def run_watermark_process(self, group_name, start_date):
        """运行水印添加处理"""
        self.gui.log("开始添加水印...")
        
        # 清空输出目录
        self.clear_directory(self.output_dir)
        
        # 获取输入目录中的图片
        image_files = []
        for ext in PROCESS_CONFIG["支持格式"]:
            image_files.extend(list(self.input_dir.glob(f"*{ext}")))
            image_files.extend(list(self.input_dir.glob(f"*{ext.upper()}")))
        
        if not image_files:
            self.gui.log("输入目录中没有找到图片文件", "ERROR")
            return 0
        
        # 按文件名排序
        def extract_number(filepath):
            match = re.search(r"(\d+)", filepath.name)
            return int(match.group(1)) if match else float('inf')
        
        image_files.sort(key=extract_number)
        
        # 处理图片
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        processed_count = 0
        
        for i, image_file in enumerate(image_files):
            try:
                output_path = self.output_dir / f"watermarked_{image_file.name}"
                date_str = current_date.strftime("%Y%m%d")
                
                self.add_date_watermark(str(image_file), str(output_path), date_str, group_name)
                current_date += timedelta(days=1)
                processed_count += 1
                
                # 更新进度
                progress = (i + 1) / len(image_files) * 100
                self.gui.progress_var.set(progress)
                self.gui.status_var.set(f"正在处理图片 {i+1}/{len(image_files)}")
                
            except Exception as e:
                self.gui.log(f"⚠️ 跳过文件 {image_file.name}，发生错误：{e}", "WARNING")
        
        self.gui.log(f"水印添加完成，生成 {processed_count} 张图片", "SUCCESS")
        return processed_count

    def move_final_images(self, group_output_folder, required_count):
        """将最终图片移动到指定班组输出目录"""
        target_dir = self.watermark_dir / group_output_folder
        target_dir.mkdir(exist_ok=True)
        
        # 清空目标目录
        self.clear_directory(target_dir)
        
        # 获取输出目录中的图片并排序
        output_images = []
        for ext in PROCESS_CONFIG["支持格式"]:
            output_images.extend(list(self.output_dir.glob(f"*{ext}")))
            output_images.extend(list(self.output_dir.glob(f"*{ext.upper()}")))
        
        output_images.sort(key=lambda x: x.name)
        
        # 移动前N张图片
        moved_count = 0
        for img_file in output_images[:required_count]:
            shutil.move(str(img_file), str(target_dir))
            moved_count += 1
            
        self.gui.log(f"已移动 {moved_count} 张图片到 {group_output_folder} 目录", "SUCCESS")
        return moved_count

    def process_single_group(self, group_key, group_config):
        """处理单个班组的完整流程"""
        self.gui.log(f"🎯 开始处理班组: {group_key}", "INFO")
        
        group_folder = group_config["folder"]
        output_folder = group_config["output_folder"]
        group_name = group_config["班组名称"]
        start_date = group_config["起始日期"]
        required_days = group_config["天数"]
        
        # 步骤1: 预处理班组图片
        if not self.process_group_images(group_folder):
            self.gui.log(f"班组 {group_key} 预处理失败", "ERROR")
            return False
            
        # 步骤2: 复制图片到输入目录
        image_count = self.copy_processed_images_to_input(group_folder)
        if image_count < required_days:
            self.gui.log(f"警告: 图片数量({image_count})少于所需天数({required_days})", "WARNING")
            
        # 步骤3: 运行水印处理
        output_count = self.run_watermark_process(group_name, start_date)
        if output_count == 0:
            return False
            
        # 步骤4: 移动最终图片
        final_count = min(required_days, output_count)
        self.move_final_images(output_folder, final_count)
        
        # 步骤5: 清理临时目录
        self.clear_directory(self.input_dir)
        self.clear_directory(self.output_dir)
        
        self.gui.log(f"✨ 班组 {group_key} 处理完成!", "SUCCESS")
        return True

    def run_full_process(self):
        """运行完整的自动化流程"""
        start_time = datetime.now()
        self.gui.log("🌟 开始完整自动化处理流程")
        
        success_count = 0
        total_groups = len(GROUPS_CONFIG)
        
        for i, (group_key, group_config) in enumerate(GROUPS_CONFIG.items()):
            try:
                # 更新总体进度
                overall_progress = i / total_groups * 100
                self.gui.progress_var.set(overall_progress)
                self.gui.status_var.set(f"正在处理班组: {group_key}")
                
                if self.process_single_group(group_key, group_config):
                    success_count += 1
                else:
                    self.gui.log(f"班组 {group_key} 处理失败", "ERROR")
            except Exception as e:
                self.gui.log(f"班组 {group_key} 处理异常: {str(e)}", "ERROR")
                
        # 最终统计
        end_time = datetime.now()
        duration = end_time - start_time
        
        self.gui.log("🎊 自动化处理流程完成!")
        self.gui.log(f"📊 处理统计: {success_count}/{total_groups} 个班组成功")
        self.gui.log(f"⏱️  总耗时: {duration}")
        
        return success_count == total_groups

def main():
    root = tk.Tk()
    app = BandukuGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("用户中断操作")

if __name__ == "__main__":
    main()