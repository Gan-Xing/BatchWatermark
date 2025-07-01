#!/usr/bin/env python3
"""
邦杜库项目图片处理GUI版本 - 修正版
完全自包含，无需外部脚本依赖
"""

import os
import sys
import shutil
import re
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFile
import threading

ImageFile.LOAD_TRUNCATED_IMAGES = True

# 默认配置模板 - 用于新检测到的班组
DEFAULT_GROUP_TEMPLATE = {
    "月份": "2025-06",
    "天数": 30,
    "起始日期": "2025-06-01"
}

# 需要排除的系统文件夹和特殊目录
EXCLUDED_FOLDERS = {
    "input_images", "output_images", "水印后", 
    ".DS_Store", "__pycache__", ".git", ".svn",
    "Thumbs.db", "temp", "tmp", "cache"
}

# 水印配置已移至BandukuGUI类的__init__方法中，支持动态修改

PROCESS_CONFIG = {
    "目标宽度": 1920,
    "目标高度": 1080,
    "支持格式": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    "输出质量": 95
}

PATHS = {
    "输入目录": "input_images",
    "输出目录": "output_images", 
    "水印后目录": "水印后"
}

class BandukuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("邦杜库项目图片处理系统")
        self.root.geometry("800x600")
        
        # 工作目录设置
        self.base_dir = None
        self.is_processing = False
        self.stop_processing = False  # 停止处理标志
        
        # 动态班组配置 - 运行时根据目录内容生成
        self.groups_config = {}
        
        # 动态水印配置 - 可在GUI中调整
        self.watermark_config = {
            "项目名称": "科特迪瓦邦杜库边境路",
            "施工区域": "项目营地", 
            "施工内容": "每日班前教育",
            "字体大小": 36,
            "背景色": (100, 149, 237, 200),
            "文字颜色": (255, 255, 255, 255)
        }
        
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
        
        self.start_btn = ttk.Button(control_frame, text="🎯 开始处理", command=self.toggle_processing)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="⚙️ 配置班组", command=self.configure_groups).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🏷️ 项目配置", command=self.configure_project).pack(side=tk.LEFT, padx=(0, 10))
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
    
    def scan_groups_from_directory(self, directory_path):
        """智能扫描目录，自动检测班组文件夹"""
        self.log("🔍 开始扫描目录，检测班组文件夹...")
        
        directory = Path(directory_path)
        detected_groups = {}
        
        # 获取所有子目录
        subdirs = [d for d in directory.iterdir() if d.is_dir()]
        
        for subdir in subdirs:
            folder_name = subdir.name
            
            # 跳过系统文件夹和特殊目录
            if folder_name in EXCLUDED_FOLDERS or folder_name.startswith('.'):
                continue
            
            # 检查文件夹中是否包含图片文件
            image_count = 0
            for ext in PROCESS_CONFIG["支持格式"]:
                image_count += len(list(subdir.glob(f"*{ext}")))
                image_count += len(list(subdir.glob(f"*{ext.upper()}")))
            
            # 如果包含图片文件，认为是班组文件夹
            if image_count > 0:
                # 使用班组名称作为默认输出文件夹编号
                output_folder = folder_name
                
                detected_groups[folder_name] = {
                    "folder": folder_name,
                    "output_folder": output_folder,
                    "班组名称": folder_name,
                    "月份": DEFAULT_GROUP_TEMPLATE["月份"],
                    "天数": DEFAULT_GROUP_TEMPLATE["天数"],
                    "起始日期": DEFAULT_GROUP_TEMPLATE["起始日期"],
                    "图片数量": image_count  # 添加图片数量信息
                }
                
                self.log(f"📁 检测到班组: {folder_name} (包含{image_count}张图片)")
        
        if detected_groups:
            self.groups_config = detected_groups
            self.log(f"✅ 成功检测到 {len(detected_groups)} 个班组", "SUCCESS")
            
            # 显示检测结果确认对话框
            self.show_groups_detection_result(detected_groups)
        else:
            self.log("⚠️ 未检测到包含图片的班组文件夹", "WARNING")
            messagebox.showwarning("警告", "在选择的目录中没有找到包含图片的班组文件夹。\n\n请确保目录结构正确：\n- 每个班组一个文件夹\n- 文件夹中包含图片文件")
            return False
        
        return True
    
    def show_groups_detection_result(self, detected_groups):
        """显示检测到的班组结果供用户确认"""
        result_window = tk.Toplevel(self.root)
        result_window.title("检测到的班组")
        result_window.geometry("600x400")
        result_window.grab_set()
        
        frame = ttk.Frame(result_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="🎯 检测到以下班组", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # 检测结果表格
        tree = ttk.Treeview(frame, columns=("班组", "图片数量", "输出编号"), show="headings", height=8)
        tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tree.heading("班组", text="班组名称")
        tree.heading("图片数量", text="图片数量")
        tree.heading("输出编号", text="输出编号")
        
        tree.column("班组", width=200)
        tree.column("图片数量", width=100)
        tree.column("输出编号", width=100)
        
        for group_name, config in detected_groups.items():
            tree.insert("", tk.END, values=(
                group_name, 
                config["图片数量"], 
                config["output_folder"]
            ))
        
        # 按钮框架
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        def confirm_groups():
            result_window.destroy()
            self.log("👍 用户确认了检测到的班组配置", "SUCCESS")
        
        def rescan_groups():
            result_window.destroy()
            if self.base_dir:
                self.scan_groups_from_directory(self.base_dir)
        
        ttk.Label(frame, text="提示：您可以在'配置班组'中调整详细设置", 
                 foreground="gray").pack(pady=(5, 0))
        
        ttk.Button(btn_frame, text="✅ 确认使用", command=confirm_groups).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="🔄 重新扫描", command=rescan_groups).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="⚙️ 详细配置", command=lambda: [result_window.destroy(), self.configure_groups()]).pack(side=tk.RIGHT)
        
    def browse_directory(self):
        directory = filedialog.askdirectory(title="选择包含班组文件夹的根目录")
        if directory:
            self.dir_var.set(directory)
            self.base_dir = Path(directory)
            self.log(f"已选择工作目录: {directory}")
            
            # 自动扫描班组文件夹
            self.scan_groups_from_directory(directory)
            
    def configure_groups(self):
        if not self.groups_config:
            messagebox.showwarning("警告", "请先选择工作目录以检测班组")
            return
            
        config_window = tk.Toplevel(self.root)
        config_window.title("班组配置")
        config_window.geometry("700x500")
        config_window.grab_set()
        
        # 创建配置界面
        frame = ttk.Frame(config_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="📋 班组配置管理", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # 配置表格
        tree = ttk.Treeview(frame, columns=("班组", "图片数", "月份", "天数", "起始日期", "输出"), show="headings", height=10)
        tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 列标题和宽度
        columns_config = [
            ("班组", "班组名称", 120),
            ("图片数", "图片数量", 80),
            ("月份", "处理月份", 100), 
            ("天数", "天数", 60),
            ("起始日期", "起始日期", 100),
            ("输出", "输出编号", 80)
        ]
        
        for col_id, col_text, col_width in columns_config:
            tree.heading(col_id, text=col_text)
            tree.column(col_id, width=col_width)
        
        def refresh_tree():
            """刷新表格显示"""
            for item in tree.get_children():
                tree.delete(item)
            for group_key, config in self.groups_config.items():
                tree.insert("", tk.END, values=(
                    config["班组名称"], 
                    config.get("图片数量", "未知"),
                    config["月份"], 
                    config["天数"], 
                    config["起始日期"],
                    config["output_folder"]
                ))
        
        # 初始填充数据
        refresh_tree()
        
        # 按钮框架
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        def update_all_config():
            """批量更新所有班组的月份配置"""
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
            for group_config in self.groups_config.values():
                group_config["月份"] = f"{year:04d}-{month:02d}"
                group_config["天数"] = days
                group_config["起始日期"] = f"{year:04d}-{month:02d}-01"
            
            refresh_tree()
            messagebox.showinfo("成功", f"已更新所有班组配置为 {year}年{month}月 ({days}天)")
            
        def edit_selected_group():
            """编辑选中的班组"""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("警告", "请先选择要编辑的班组")
                return
                
            item = tree.item(selection[0])
            group_name = item['values'][0]
            
            if group_name not in self.groups_config:
                messagebox.showerror("错误", "找不到该班组配置")
                return
                
            self.edit_group_dialog(group_name, refresh_tree)
            
        def rescan_groups():
            """重新扫描班组"""
            if self.base_dir:
                config_window.destroy()
                self.scan_groups_from_directory(self.base_dir)
            else:
                messagebox.showwarning("警告", "请先选择工作目录")
                
        def remove_selected_group():
            """移除选中的班组"""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("警告", "请先选择要移除的班组")
                return
                
            item = tree.item(selection[0])
            group_name = item['values'][0]
            
            if messagebox.askyesno("确认", f"确定要移除班组 '{group_name}' 吗？"):
                if group_name in self.groups_config:
                    del self.groups_config[group_name]
                    # 重新分配输出编号
                    for i, config in enumerate(self.groups_config.values(), 1):
                        config["output_folder"] = str(i)
                    refresh_tree()
                    self.log(f"已移除班组: {group_name}")
        
        # 按钮布局
        ttk.Button(btn_frame, text="📅 批量设置月份", command=update_all_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="✏️ 编辑选中", command=edit_selected_group).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🔄 重新扫描", command=rescan_groups).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ 移除选中", command=remove_selected_group).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="✅ 完成", command=config_window.destroy).pack(side=tk.RIGHT)
        
    def edit_group_dialog(self, group_name, refresh_callback):
        """编辑单个班组的详细配置"""
        config = self.groups_config[group_name]
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"编辑班组: {group_name}")
        edit_window.geometry("400x300")
        edit_window.grab_set()
        
        frame = ttk.Frame(edit_window, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"编辑班组: {group_name}", font=("Arial", 12, "bold")).pack(pady=(0, 15))
        
        # 输入字段
        fields = [
            ("班组名称", "班组名称", config["班组名称"]),
            ("处理月份", "月份", config["月份"]),
            ("处理天数", "天数", str(config["天数"])),
            ("起始日期", "起始日期", config["起始日期"]),
            ("输出编号", "output_folder", config["output_folder"])
        ]
        
        entries = {}
        for label_text, key, value in fields:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(row_frame, text=label_text, width=12).pack(side=tk.LEFT)
            entry = ttk.Entry(row_frame, width=25)
            entry.insert(0, str(value))
            entry.pack(side=tk.LEFT, padx=(10, 0))
            entries[key] = entry
        
        def save_changes():
            try:
                # 验证并保存更改
                new_name = entries["班组名称"].get().strip()
                new_month = entries["月份"].get().strip()
                new_days = int(entries["天数"].get().strip())
                new_start_date = entries["起始日期"].get().strip()
                new_output = entries["output_folder"].get().strip()
                
                if not all([new_name, new_month, new_start_date, new_output]):
                    messagebox.showerror("错误", "所有字段都必须填写")
                    return
                
                # 验证日期格式
                try:
                    datetime.strptime(new_start_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("错误", "日期格式应为 YYYY-MM-DD")
                    return
                
                # 更新配置
                if new_name != group_name:
                    # 班组名称改变，需要更新字典key
                    self.groups_config[new_name] = self.groups_config.pop(group_name)
                    config = self.groups_config[new_name]
                    config["folder"] = new_name
                else:
                    # 班组名称未改变，直接获取配置
                    config = self.groups_config[group_name]
                
                config["班组名称"] = new_name
                config["月份"] = new_month
                config["天数"] = new_days
                config["起始日期"] = new_start_date
                config["output_folder"] = new_output
                
                edit_window.destroy()
                refresh_callback()
                self.log(f"已更新班组配置: {new_name}")
                
            except ValueError as e:
                messagebox.showerror("错误", f"输入格式错误: {e}")
        
        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="💾 保存", command=save_changes).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="❌ 取消", command=edit_window.destroy).pack(side=tk.RIGHT)
        
    def open_results(self):
        if not self.base_dir:
            messagebox.showwarning("警告", "请先选择工作目录")
            return
            
        result_dir = self.base_dir / "水印后"
        if result_dir.exists():
            if sys.platform == "win32":
                os.startfile(result_dir)
            elif sys.platform == "darwin":
                os.system(f"open '{result_dir}'")
            else:
                os.system(f"xdg-open '{result_dir}'")
        else:
            messagebox.showinfo("提示", "结果目录不存在，请先进行处理")
    
    def configure_project(self):
        """配置项目信息"""
        config_window = tk.Toplevel(self.root)
        config_window.title("项目配置")
        config_window.geometry("450x300")
        config_window.grab_set()
        
        frame = ttk.Frame(config_window, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="🏷️ 项目信息配置", font=("Arial", 14, "bold")).pack(pady=(0, 15))
        
        # 输入字段
        fields = [
            ("项目名称", "项目名称", self.watermark_config["项目名称"]),
            ("施工区域", "施工区域", self.watermark_config["施工区域"]),
            ("施工内容", "施工内容", self.watermark_config["施工内容"])
        ]
        
        entries = {}
        for label_text, key, value in fields:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=8)
            
            ttk.Label(row_frame, text=label_text, width=12).pack(side=tk.LEFT)
            entry = ttk.Entry(row_frame, width=30)
            entry.insert(0, str(value))
            entry.pack(side=tk.LEFT, padx=(10, 0))
            entries[key] = entry
        
        def save_project_config():
            try:
                # 更新配置
                self.watermark_config["项目名称"] = entries["项目名称"].get().strip()
                self.watermark_config["施工区域"] = entries["施工区域"].get().strip()
                self.watermark_config["施工内容"] = entries["施工内容"].get().strip()
                
                if not all([self.watermark_config["项目名称"], 
                           self.watermark_config["施工区域"], 
                           self.watermark_config["施工内容"]]):
                    messagebox.showerror("错误", "所有字段都必须填写")
                    return
                
                config_window.destroy()
                self.log("已更新项目配置")
                messagebox.showinfo("成功", "项目配置已保存")
                
            except Exception as e:
                messagebox.showerror("错误", f"保存配置时出错: {e}")
        
        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="💾 保存", command=save_project_config).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="❌ 取消", command=config_window.destroy).pack(side=tk.RIGHT)
        
    def toggle_processing(self):
        """切换处理状态：开始或停止"""
        if self.is_processing:
            # 当前正在处理，设置停止标志
            self.stop_processing = True
            self.start_btn.config(text="⏳ 正在停止...", state="disabled")
            self.log("⏹️ 用户请求停止处理...", "WARNING")
        else:
            # 当前未处理，开始处理
            self.start_processing()
    
    def start_processing(self):
        if not self.base_dir:
            messagebox.showwarning("警告", "请先选择工作目录")
            return
            
        if not self.groups_config:
            messagebox.showwarning("警告", "没有检测到班组，请重新选择目录或检查目录结构")
            return
            
        if self.is_processing:
            messagebox.showinfo("提示", "正在处理中，请等待完成")
            return
            
        # 重置停止标志并开始处理
        self.stop_processing = False
        self.is_processing = True
        self.start_btn.config(text="⏹️ 停止处理", state="normal")
        thread = threading.Thread(target=self.run_processing, daemon=True)
        thread.start()
        
    def run_processing(self):
        try:
            processor = BandukuProcessor(self.base_dir, self, self.groups_config)
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
            self.start_btn.config(text="🎯 开始处理", state="normal")
            if self.stop_processing:
                self.status_var.set("已停止处理")
                self.log("⏹️ 处理已停止", "WARNING")
            else:
                self.status_var.set("处理完成")
            self.progress_var.set(0)

class BandukuProcessor:
    def __init__(self, base_dir, gui, groups_config):
        self.base_dir = Path(base_dir)
        self.gui = gui
        self.groups_config = groups_config
        self.input_dir = self.base_dir / PATHS["输入目录"]
        self.output_dir = self.base_dir / PATHS["输出目录"]
        self.watermark_dir = self.base_dir / PATHS["水印后目录"]
        
        # 确保目录存在
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.watermark_dir.mkdir(exist_ok=True)
        
        self.gui.log("🚀 邦杜库项目图片处理系统启动")
        self.gui.log(f"📁 工作目录: {self.base_dir}")
        self.gui.log(f"📊 配置班组数量: {len(self.groups_config)}")

    def clear_directory(self, directory):
        """清空目录"""
        if directory.exists():
            for item in directory.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            self.gui.log(f"已清空目录: {directory.name}")

    def count_images_in_directory(self, directory):
        """统计目录中的图片数量"""
        if not directory.exists():
            return 0
        
        image_count = 0
        for ext in PROCESS_CONFIG["支持格式"]:
            image_count += len(list(directory.glob(f"*{ext}")))
            image_count += len(list(directory.glob(f"*{ext.upper()}")))
        return image_count

    def rename_images_in_directory(self, directory):
        """重命名目录中的图片文件"""
        self.gui.log("开始重命名图片文件...")
        
        # 获取所有图片文件
        image_files = []
        for ext in PROCESS_CONFIG["支持格式"]:
            image_files.extend(list(directory.glob(f"*{ext}")))
            image_files.extend(list(directory.glob(f"*{ext.upper()}")))
        
        if not image_files:
            self.gui.log("目录中没有找到图片文件", "WARNING")
            return False
        
        # 按名称排序
        image_files.sort()
        
        # 重命名文件
        renamed_count = 0
        for index, image_file in enumerate(image_files, 1):
            try:
                # 统一转换为png格式
                new_name = f'image{str(index).zfill(3)}.png'
                new_path = directory / new_name
                
                # 如果新文件名已存在，跳过
                if new_path.exists() and new_path != image_file:
                    continue
                    
                # 如果不是png格式，需要转换
                if image_file.suffix.lower() != '.png':
                    # 使用PIL转换格式
                    with Image.open(image_file) as img:
                        # 转换为RGB模式（去除Alpha通道）
                        if img.mode in ('RGBA', 'LA', 'P'):
                            img = img.convert('RGB')
                        img.save(new_path, 'PNG', quality=PROCESS_CONFIG["输出质量"])
                    
                    # 删除原文件
                    image_file.unlink()
                    self.gui.log(f"已转换并重命名: {image_file.name} -> {new_name}")
                else:
                    # 如果已经是png且名称正确，跳过
                    if image_file.name != new_name:
                        image_file.rename(new_path)
                        self.gui.log(f"已重命名: {image_file.name} -> {new_name}")
                
                renamed_count += 1
            except Exception as e:
                self.gui.log(f"重命名 {image_file.name} 时发生错误: {str(e)}", "ERROR")
        
        self.gui.log(f"图片重命名完成，处理了 {renamed_count} 个文件")
        return True

    def resize_and_shuffle_images(self, directory):
        """调整图片尺寸并随机打乱顺序"""
        self.gui.log("开始调整图片尺寸并随机化...")
        
        # 获取所有png图片文件
        image_files = list(directory.glob("image*.png"))
        
        if not image_files:
            self.gui.log("目录中没有找到图片文件", "WARNING")
            return False
        
        # 按文件名排序
        image_files.sort()
        
        try:
            # 首先调整所有图片尺寸
            target_width = PROCESS_CONFIG["目标宽度"]
            target_height = PROCESS_CONFIG["目标高度"]
            
            for img_file in image_files:
                try:
                    with Image.open(img_file) as img:
                        # 调整图片尺寸
                        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                        img_resized.save(img_file, 'PNG', quality=PROCESS_CONFIG["输出质量"])
                except Exception as e:
                    self.gui.log(f"调整 {img_file.name} 尺寸时出错: {str(e)}", "ERROR")
            
            self.gui.log("图片尺寸调整完成")
            
            # 随机打乱文件顺序
            random.shuffle(image_files)
            
            # 创建临时文件名映射
            temp_mapping = {}
            for i, img_file in enumerate(image_files):
                temp_name = directory / f"temp_{i}.png"
                temp_mapping[img_file] = temp_name
            
            # 先重命名为临时文件
            for original, temp in temp_mapping.items():
                original.rename(temp)
            
            # 再按新顺序重命名
            for i, temp_file in enumerate(temp_mapping.values(), 1):
                final_name = directory / f"image{str(i).zfill(3)}.png"
                temp_file.rename(final_name)
            
            self.gui.log(f"图片顺序随机化完成，共处理 {len(image_files)} 个文件")
            return True
            
        except Exception as e:
            self.gui.log(f"图片处理过程中出错: {str(e)}", "ERROR")
            return False

    def process_group_images(self, group_folder):
        """处理单个班组的图片 - 纯Python实现"""
        group_path = self.base_dir / group_folder
        
        if not group_path.exists():
            self.gui.log(f"班组目录不存在: {group_folder}", "ERROR")
            return False

        self.gui.log(f"开始处理班组: {group_folder}")
        
        # 步骤1: 图片重命名和格式标准化
        if not self.rename_images_in_directory(group_path):
            self.gui.log("图片重命名失败", "ERROR")
            return False
        
        # 步骤2: 图片尺寸调整和随机化
        if not self.resize_and_shuffle_images(group_path):
            self.gui.log("图片处理失败", "ERROR")
            return False
            
        self.gui.log(f"班组 {group_folder} 图片预处理完成", "SUCCESS")
        return True

    def copy_processed_images_to_input(self, group_folder):
        """将处理好的图片复制到input目录"""
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

        # 水印内容 - 使用动态配置
        text_lines = [
            (self.gui.watermark_config["项目名称"], (100, 149, 237)),
            f"施 工 区 域：{self.gui.watermark_config['施工区域']}",
            f"施 工 内 容：{self.gui.watermark_config['施工内容']}",
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
            # 检查是否需要停止处理
            if self.gui.stop_processing:
                self.gui.log("⏹️ 水印处理被中断", "WARNING")
                break
                
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
        
        # 步骤1: 预处理班组图片（纯Python实现）
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
        total_groups = len(self.groups_config)
        
        for i, (group_key, group_config) in enumerate(self.groups_config.items()):
            # 检查是否需要停止处理
            if self.gui.stop_processing:
                self.gui.log("⏹️ 收到停止信号，中断处理", "WARNING")
                break
                
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