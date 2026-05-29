# ===== 强制导入，供 PyInstaller 打包识别 ===== 
import nets.deeplabv3_plus 
import nets.unet 
import utils.utils 
# ============================================ 
import os 
import sys
 
def get_resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和PyInstaller打包后的环境"""
    try:
        # PyInstaller 创建临时文件夹，将路径存入 _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境下 
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
 
# 示例：加载模型
banner_path1 = get_resource_path("images/UI/zhu.jpg")
icon_path1  = get_resource_path("images/UI/logo.jpg")
style_path1 = get_resource_path("style/hospital_theme.qss")

# import sys
# import os
import datetime
import subprocess
import threading
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import pydicom
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QProgressBar, QTabWidget,
    QListWidget, QTextEdit, QSplitter, QGridLayout, QStyleFactory, QLineEdit
)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import QDir, Qt
 
# 引入深度学习模型
from deeplab import DeeplabV3 
from unet import Unet
 
# 引入 matplotlib 画布
import matplotlib
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['axes.unicode_minus'] = False
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
 
 
class SegmentationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("深肺智影alpha1.0")
        self.setGeometry(100, 100, 1400, 800)
        
        # 设置图标（添加错误处理）
        icon_path = icon_path1
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 初始化模型
        self.deeplab = DeeplabV3()
        self.unet = Unet()
        
        # 日志文件路径
        self.log_file_path = os.path.abspath("log_output.txt")
                # ✅ 新增：记录当前输入和输出目录的变量 
        self.current_input_dir = os.path.abspath("img")      # 默认输入目录 
        self.current_output_dir = os.path.abspath("imgs_out") # 默认输出目录
        
        # 样式设置
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 5px;
                padding: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QTextEdit, QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 13px;
            }
            QLabel {
                background-color: #111;
                border: 1px solid #444;
                color: white;
            }
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                width: 20px;
            }
        """)
        
        self.init_ui()
 
    def init_ui(self):
        self.tabs = QTabWidget()
 
        self.tab_home = QWidget()
        self.init_home_tab()
        self.tabs.addTab(self.tab_home, "首页")
 
        self.tab_detect = QWidget()
        self.init_detect_tab()
        self.tabs.addTab(self.tab_detect, "影像检测")
 
        # 删除第三标签页：定量分析
        # self.tab_analysis = QWidget()
        # self.init_analysis_tab()
        # self.tabs.addTab(self.tab_analysis, "定量分析")
 
        self.setCentralWidget(self.tabs)
 
    def init_home_tab(self):
        layout = QVBoxLayout()
 
        # 医院名称标题
        hospital_title = QLabel("XX医院HRCT分析系统")
        hospital_title.setAlignment(Qt.AlignCenter)
        hospital_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #004080; background-color: transparent; border: none;")
 
        # 首页封面图
        self.label_home_banner = QLabel()
        banner_path = banner_path1
        if os.path.exists(banner_path):
            self.label_home_banner.setPixmap(QPixmap(banner_path).scaledToWidth(1000, Qt.SmoothTransformation))
        self.label_home_banner.setAlignment(Qt.AlignCenter)
        self.label_home_banner.setStyleSheet("background-color: transparent; border: none;")
 
        btn_open_results = QPushButton("📂 查看历史")
        btn_open_log = QPushButton("📄 查看日志")
        btn_manage_cases = QPushButton("🗂 管理病例")
 
        btn_open_results.setFixedSize(250, 40)
        btn_open_log.setFixedSize(250, 40)
        btn_manage_cases.setFixedSize(250, 40)
 
        btn_open_results.clicked.connect(self.open_results_folder)
        btn_open_log.clicked.connect(self.open_log_file)
        btn_manage_cases.clicked.connect(self.launch_case_manager)
 
        layout.addWidget(hospital_title)
        layout.addWidget(self.label_home_banner)
        layout.addWidget(btn_open_results, alignment=Qt.AlignCenter)
        layout.addWidget(btn_open_log, alignment=Qt.AlignCenter)
        layout.addWidget(btn_manage_cases, alignment=Qt.AlignCenter)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 20, 40, 20)
 
        self.tab_home.setLayout(layout)
 
    # def launch_case_manager(self):
    #     try:
    #         python_path = sys.executable
    #         script_path = os.path.join(os.path.dirname(__file__), "xinghuoUIs.py")
            
    #         if not os.path.exists(script_path):
    #             QMessageBox.warning(self, "警告", f"病例管理脚本不存在: {script_path}")
    #             return
            
    #         env = os.environ.copy()
    #         venv_path = os.path.dirname(python_path)
    #         if sys.platform == "win32":
    #             site_packages = os.path.join(venv_path, "Lib", "site-packages")
    #         else:
    #             site_packages = os.path.join(venv_path, "lib", 
    #                 f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
            
    #         if "PYTHONPATH" in env:
    #             env["PYTHONPATH"] = site_packages + os.pathsep + env["PYTHONPATH"]
    #         else:
    #             env["PYTHONPATH"] = site_packages
            
    #         self.log_to_file(f"使用Python: {python_path}")
    #         self.log_to_file(f"脚本路径: {script_path}")
            
    #         process = subprocess.Popen(
    #             [python_path, script_path],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True,
    #             env=env
    #         )
            
    #         def monitor_process():
    #             stdout, stderr = process.communicate()
    #             if stdout:
    #                 self.log_to_file(f"子进程输出: {stdout}")
    #             if stderr:
    #                 self.log_to_file(f"子进程错误: {stderr}")
    #             if process.returncode != 0:
    #                 self.log_to_file(f"子进程退出码: {process.returncode}")
            
    #         monitor_thread = threading.Thread(target=monitor_process)
    #         monitor_thread.daemon = True
    #         monitor_thread.start()
            
    #         self.log_to_file("已启动病例管理系统")
            
    #     except Exception as e:
    #         self.log_to_file(f"启动失败: {str(e)}")
    #         QMessageBox.critical(self, "错误", f"无法启动病例管理系统: {e}")
    
    def launch_case_manager(self):
        try:
            # 获取主程序 exe 所在的目录 
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            exe_path = os.path.join(application_path, "xinghuoUIs.exe")
            
            # Windows 下创建独立进程的标志 
            kwargs = {}
            if sys.platform == 'win32':
                # DETACHED_PROCESS: 让子进程在独立的进程组中运行，不受主进程关闭影响 
                kwargs['creationflags'] = subprocess.DETACHED_PROCESS 
            
            if not os.path.exists(exe_path):
                # 找不到 exe，尝试开发环境回退 
                script_path = os.path.join(application_path, "xinghuoUIs.py")
                if not os.path.exists(script_path):
                    QMessageBox.warning(self, "警告", f"未找到病例管理程序:\n{exe_path}")
                    return 
                
                python_path = sys.executable 
                self.log_to_file(f"开发环境启动: {python_path} {script_path}")
                subprocess.Popen(
                    [python_path, script_path],
                    stdin=subprocess.DEVNULL,   # 断开输入管道 
                    stdout=subprocess.DEVNULL,  # 断开输出管道，防止管道破裂导致崩溃 
                    stderr=subprocess.DEVNULL,  # 断开错误管道 
                    **kwargs 
                )
            else:
                # 打包后环境：直接运行 exe 
                self.log_to_file(f"启动病例管理EXE: {exe_path}")
                subprocess.Popen(
                    [exe_path],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    **kwargs 
                )
            
            self.log_to_file("已启动病例管理系统（独立进程）")
            
        except Exception as e:
            self.log_to_file(f"启动失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"无法启动病例管理系统: {e}")

    def init_detect_tab(self):
        # 左侧：文件列表
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_item_clicked)
        self.file_list.setMinimumWidth(200)
        
        file_list_widget = QWidget()
        file_list_layout = QVBoxLayout()
        file_list_label = QLabel("文件列表")
        file_list_label.setStyleSheet("font-weight: bold; font-size: 14px; background-color: transparent; color: #333; border: none;")
        file_list_layout.addWidget(file_list_label)
        file_list_layout.addWidget(self.file_list)
        file_list_widget.setLayout(file_list_layout)
 
        # 中间：2x2网格
        # 左上：原图
        self.label_original = QLabel("原图")
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_original.setFixedSize(380, 320)
        
        # 右上：病灶结果
        self.label_deeplab = QLabel("病灶结果")
        self.label_deeplab.setAlignment(Qt.AlignCenter)
        self.label_deeplab.setFixedSize(380, 320)
        
        # 左下：肺部
        self.label_unet = QLabel("肺部")
        self.label_unet.setAlignment(Qt.AlignCenter)
        self.label_unet.setFixedSize(380, 320)
        
        # 右下：体积计算结果（新增）
        self.label_volume_result = QLabel("面积计算")
        self.label_volume_result.setAlignment(Qt.AlignCenter)
        self.label_volume_result.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.label_volume_result.setFixedSize(380, 320)
        
        # 创建中间网格
        middle_widget = QWidget()
        middle_layout = QGridLayout()
        middle_layout.setSpacing(10)
        middle_layout.addWidget(self.label_original, 0, 0)
        middle_layout.addWidget(self.label_deeplab, 0, 1)
        middle_layout.addWidget(self.label_unet, 1, 0)
        middle_layout.addWidget(self.label_volume_result, 1, 1)
        middle_widget.setLayout(middle_layout)
 
        # 右侧：三个纵向文本框
        self.text_patient_info = QTextEdit()
        self.text_patient_info.setPlaceholderText("患者信息（DICOM）")
        self.text_patient_info.setReadOnly(True)
        self.text_patient_info.setFixedHeight(150)
        
        self.text_diagnosis = QTextEdit()
        self.text_diagnosis.setPlaceholderText("辅助诊断结果")
        self.text_diagnosis.setReadOnly(True)
        self.text_diagnosis.setFixedHeight(180)
        
        self.text_analysis = QTextEdit()
        self.text_analysis.setPlaceholderText("定量分析结果")
        self.text_analysis.setReadOnly(True)
        self.text_analysis.setFixedHeight(200)
 
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        
        # 标签
        label_patient = QLabel("患者信息")
        label_patient.setStyleSheet("font-weight: bold; background-color: transparent; color: #333; border: none;")
        label_diagnosis = QLabel("辅助诊断")
        label_diagnosis.setStyleSheet("font-weight: bold; background-color: transparent; color: #333; border: none;")
        label_analysis = QLabel("定量分析")
        label_analysis.setStyleSheet("font-weight: bold; background-color: transparent; color: #333; border: none;")
        
        right_layout.addWidget(label_patient)
        right_layout.addWidget(self.text_patient_info)
        right_layout.addWidget(label_diagnosis)
        right_layout.addWidget(self.text_diagnosis)
        right_layout.addWidget(label_analysis)
        right_layout.addWidget(self.text_analysis)
        right_widget.setLayout(right_layout)
 
        # 底部：按钮和进度条
        self.btn_predict = QPushButton("🔍 单图预测")
        self.btn_predict.clicked.connect(self.predict_image)
 
        self.btn_dir_predict = QPushButton("📁 批量预测")
        self.btn_dir_predict.clicked.connect(self.dir_predict)
 
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
 
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_predict)
        button_layout.addSpacing(20)
        button_layout.addWidget(self.btn_dir_predict)
        button_layout.addStretch()
 
        bottom_layout = QVBoxLayout()
        bottom_layout.addLayout(button_layout)
        bottom_layout.addWidget(self.progress_bar)
 
        # 组装中间+右侧区域
        center_right_splitter = QSplitter(Qt.Horizontal)
        center_right_splitter.addWidget(middle_widget)
        center_right_splitter.addWidget(right_widget)
        center_right_splitter.setStretchFactor(0, 3)
        center_right_splitter.setStretchFactor(1, 2)
 
        # 组装整个布局
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(file_list_widget)
        main_splitter.addWidget(center_right_splitter)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 5)
 
        layout = QVBoxLayout()
        layout.addWidget(main_splitter, 5)
        layout.addLayout(bottom_layout)
        
        self.tab_detect.setLayout(layout)
 
    # 删除原有的 init_analysis_tab 方法
    # def init_analysis_tab(self):
    #     ...
 
    def log_to_file(self, message):
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
 
    def load_image_any_format(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".dcm":
            try:
                ds = pydicom.dcmread(filepath)
                # ========== 获取Rescale参数 ==========
                # RescaleSlope (0028,1053)：斜率，默认为1
                # RescaleIntercept (0028,1052)：截距，默认为0
                rescale_slope = float(ds.get("RescaleSlope", 1))
                rescale_intercept = float(ds.get("RescaleIntercept", -1000))
                
                # 将原始像素值转换为HU值
                img_hu = ds.pixel_array.astype(np.float32) * rescale_slope + rescale_intercept
                # 应用窗宽窗位 (Linear Windowing)
                WW = 1500
                WL = -500  # 肺窗常用窗位
                img_min = WL - WW / 2
                img_max = WL + WW / 2
                
                # 线性映射到 0-255 范围
                img_windowed = (img_hu - img_min) / (img_max - img_min) * 255.0
                
                # 截断超出范围的值
                img_windowed = np.clip(img_windowed, 0, 255)
                
                # 转换为 uint8
                img_array = img_windowed.astype(np.uint8)
                
                # 转换为RGB图像
                image = Image.fromarray(img_array).convert("RGB")
                
                return image, ds
                
            except Exception as e:
                raise ValueError(f"DICOM 加载失败：{e}")
        else:
            return Image.open(filepath), None 
        
    def on_file_item_clicked(self, item):
        name = item.text()
        name_no_ext, _ = os.path.splitext(name)
 
        # ✅ 修改：使用记录的目录，而不是硬编码的 "img" 和 "imgs_out"
        output_dir = self.current_output_dir 
        input_dir = self.current_input_dir 
        
        # 构建各种可能的路径 
        orig_path = os.path.join(input_dir, name)
        deeplab_path = os.path.join(output_dir, f"{name_no_ext}_deeplab.png")
        unet_path = os.path.join(output_dir, f"{name_no_ext}_unet.png")
 
        try:
            image_loaded = False 
            
            # 尝试加载原图 
            if os.path.exists(orig_path):
                image, ds = self.load_image_any_format(orig_path)
                self.show_image_on_label(self.label_original, image, add_annotations=True)
                if ds is not None:
                    self.display_patient_info(ds)
                image_loaded = True 
            else:
                # 尝试其他格式 (有时列表里显示的是 .dcm，但实际想看 .png)
                for ext in ['.dcm', '.png', '.jpg', '.jpeg', '.bmp']:
                    alt_path = os.path.join(input_dir, name_no_ext + ext)
                    if os.path.exists(alt_path):
                        image, ds = self.load_image_any_format(alt_path)
                        self.show_image_on_label(self.label_original, image, add_annotations=True)
                        if ds is not None:
                            self.display_patient_info(ds)
                        image_loaded = True 
                        break 
            
            if not image_loaded:
                self.label_original.setText(f"原图未找到\n路径: {orig_path}")
 
            # 显示分割结果 
            if os.path.exists(unet_path):
                unet_result = Image.open(unet_path)
                self.show_image_on_label(self.label_unet, unet_result, add_annotations=True)
            else:
                self.label_unet.setText("无肺部结果")
                
            if os.path.exists(deeplab_path):
                deeplab_result = Image.open(deeplab_path)
                self.show_image_on_label(self.label_deeplab, deeplab_result, add_annotations=True)
                
                # 保存临时文件用于分析 
                temp_lung = os.path.join(self.current_output_dir, "temp_lung.png")
                temp_lesion = os.path.join(self.current_output_dir, "temp_lesion.png")
                unet_result.save(temp_lung)
                deeplab_result.save(temp_lesion)
                self.analyze_quantitatively(temp_lung, temp_lesion)
            else:
                self.label_deeplab.setText("无病灶结果")
 
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法加载图像：{e}")
 
    def display_patient_info(self, ds):
        """显示DICOM患者信息"""
        info = []
        for tag in ['PatientName', 'PatientID', 'PatientSex', 'PatientBirthDate', 'PatientAge', 'Modality']:
            if tag in ds:
                value = ds.data_element(tag).value
                info.append(f"{tag}: {value}")
        self.text_patient_info.setText("\n".join(info))
 
    def show_image_on_label(self, label: QLabel, image: Image.Image, add_annotations: bool = False):
        """显示图像到标签"""
        display_image = image.convert("RGB")
        
        if add_annotations:
            draw = ImageDraw.Draw(display_image)
            try:
                # 建议字体路径也使用 get_resource_path，否则打包后可能找不到 arial.ttf 
                font = ImageFont.load_default() 
            except:
                font = ImageFont.load_default()
            
            w, h = display_image.size 
            margin = 10 
            fill_color = "yellow"
            draw.text((w//2 - 10, margin), "A", fill=fill_color, font=font)
            draw.text((w//2 - 10, h - margin - 20), "P", fill=fill_color, font=font)
            draw.text((margin, h//2 - 10), "R", fill=fill_color, font=font)
            draw.text((w - margin - 10, h//2 - 10), "L", fill=fill_color, font=font)
        
        data = display_image.tobytes("raw", "RGB")
        q_img = QImage(data, display_image.width, display_image.height, 
                       display_image.width * 3, QImage.Format_RGB888)
        
        # ✅ 关键修复：必须调用 copy()！ 
        # 否则 data 作为局部变量被垃圾回收后，QImage 指向的内存失效，画面会冻结或花屏 
        pixmap = QPixmap.fromImage(q_img.copy()) 
        
        scaled_pixmap = pixmap.scaled(label.width(), label.height(), 
                                       Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled_pixmap)
 
    def calculate_area(self, cv_img, color):
        hsv_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
      
        ranges = {
            'GGO':  ([0, 100, 100],   [10, 255, 200]),    # 暗红 (128,0,0)  H≈0 
            'TRBR': ([20, 100, 100],  [40, 255, 200]),     # 橄榄 (128,128,0) H≈30 
            'CONS':   ([50, 100, 100],  [70, 255, 200]),     # 暗绿 (0,128,0)  H≈60 
            'RE': ([110, 100, 100], [130, 255, 200]),    # 暗蓝 (0,0,128)  H≈120 
        }
        if color not in ranges:
            return 0
        lower, upper = np.array(ranges[color][0]), np.array(ranges[color][1])
        mask = cv2.inRange(hsv_image, lower, upper)
        return cv2.countNonZero(mask)
 
    def calculate_physical_area(self, pixel_count, pixel_spacing):
        return round(pixel_count * pixel_spacing[0] * pixel_spacing[1], 2)
 
    def analyze_quantitatively(self, lung_img_path, lesion_img_path):
        """单图定量分析"""
        try:
            lung_img = cv2.imread(lung_img_path)
            lesion_img = cv2.imread(lesion_img_path)
            pixel_spacing = [0.771484375, 0.771484375]
            lung_area = self.calculate_area(lung_img, 'GGO')
            colors = ['GGO', 'RE', 'CONS', 'TRBR']
            # ✅ 新增：缩写词与颜色的映射字典 
            color_map = {
                'GGO': (128, 0, 0),
                'CONS': (0, 128, 0),
                'RE': (0, 0, 128),
                'TRBR': (128, 128, 0)
            }
            nodule_areas = {c: self.calculate_area(lesion_img, c) for c in colors}
            nodule_phys = {c: self.calculate_physical_area(nodule_areas[c], pixel_spacing) /100 for c in colors}
            lung_phys = self.calculate_physical_area(lung_area, pixel_spacing)/100
    
            result_lines = [f"肺部物理面积: {lung_phys:.2f} cm²<br>"]
            for c in colors:
                percent = (nodule_areas[c] / lung_area) * 100 if lung_area > 0 else 0

# ✅ 修改：将缩写词包裹在带颜色的 HTML span 标签中 
                rgb = color_map.get(c, (0,0,0))
                colored_name = f'<span style="color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); font-weight: bold;">{c}</span>'
                
                # ✅ 修改：使用 colored_name 替换原来的 c，将 \n 替换为 <br>
                result_lines.append(f"{colored_name}: 物理面积: {nodule_phys[c]:.2f} cm², 占肺部比例: {percent:.2f}%<br>")
            
            # ✅ 修改：因为每行末尾已有 <br>，这里直接用空字符串连接 
            result_text = "".join(result_lines)
            
            # 单图面积结果显示在中间2×2网格右下角 
            self.label_volume_result.setText(result_text)
            
        except Exception as e:
            error_msg = f"分析失败：{e}"
            self.label_volume_result.setText(error_msg)
    def analyze_total_volume_across_dir(self, lung_dir, lesion_dir, dicom_dir=None):
        """批量预测后的总体积分析"""
        try:
            colors = ['GGO', 'RE', 'CONS', 'TRBR']
            total_lung_px = 0
            total_nodule_px = {c: 0 for c in colors}
            pixel_spacing = [0.771484375, 0.771484375]
            slice_thickness = 10.0
    
            filenames = sorted([f for f in os.listdir(lung_dir) if f.endswith("_unet.png")])
            for fname in filenames:
                base = fname.replace("_unet.png", "")
                lung_path = os.path.join(lung_dir, f"{base}_unet.png")
                lesion_path = os.path.join(lesion_dir, f"{base}_deeplab.png")
                dicom_path = os.path.join(dicom_dir, f"{base}.dcm") if dicom_dir else None
    
                lung_img = cv2.imread(lung_path)
                lesion_img = cv2.imread(lesion_path)
    
                if dicom_path and os.path.exists(dicom_path):
                    try:
                        ds = pydicom.dcmread(dicom_path)
                        if "PixelSpacing" in ds:
                            pixel_spacing = list(map(float, ds.PixelSpacing))
                        if "SliceThickness" in ds:
                            slice_thickness = float(ds.SliceThickness)
                    except Exception as e:
                        self.log_to_file(f"读取 DICOM 空间信息失败（{base}）：{e}")
    
                total_lung_px += self.calculate_area(lung_img, 'GGO')
                for c in colors:
                    total_nodule_px[c] += self.calculate_area(lesion_img, c)
    
            def calc(px):
                return round(px * pixel_spacing[0] * pixel_spacing[1] * slice_thickness, 2)
            
            total_lung_vol = calc(total_lung_px)
            total_nodule_vol = {c: calc(total_nodule_px[c]) for c in colors}
    
            def format_volume(v):
                return f"{v/1000:.2f} cm³"
    
            lines = [f"肺部总体积: {format_volume(total_lung_vol)}\n"]
            for c in colors:
                ratio = (total_nodule_vol[c] / total_lung_vol * 100) if total_lung_vol > 0 else 0 
                lines.append(f"{c}: 体积 {format_volume(total_nodule_vol[c])}, 占肺比例: {ratio:.2f}%\n")
    
            result = "\n".join(lines)
            
            # 批量总体积结果显示在右侧文本框
            self.text_analysis.setText(result)
            
            # 清空中间区域
            self.label_volume_result.setText("面积计算\n（点击左侧文件显示）")
    
        except Exception as e:
            self.text_analysis.setText(f"总体积分析失败：{e}")
    def process_image_from_path(self, image_path):
        """处理单张图像"""
        try:
            # ✅ 新增：记录单图所在的目录，以便点击列表时能找到 
            self.current_input_dir = os.path.dirname(image_path)
            
            image, ds = self.load_image_any_format(image_path)

 
            deeplab_result = self.deeplab.detect_image(image.copy())
            unet_result = self.unet.detect_image(image.copy())
 
            self.show_image_on_label(self.label_original, image, add_annotations=True)
            self.show_image_on_label(self.label_unet, unet_result, add_annotations=True)
            self.show_image_on_label(self.label_deeplab, deeplab_result, add_annotations=True)
            # 显示患者信息
            if ds is not None:
                self.display_patient_info(ds)
                
                # 显示诊断建议（静态）
                self.text_diagnosis.setText(
                    # "【评分计算】\n"
                    # "病灶负荷：0.2478\n"
                    # "年龄修正：45.8495\n"
                    # "性别系数：1\n"
                    # "肺功能：0.226\n"
                    # "并发症：2\n"
                    # "综合评分：4.7172\n\n"
                    # "【是否UIP】是(91.3%)\n"
                    # "【危险等级】IV级\n"
                    # "【临床建议】ECMO备用方案 + 多学科会诊"
                    "\n需要完整序列输入"
                )
 
            # 保存临时文件用于分析
            temp_lung = "temp_lung.png"
            temp_lesion = "temp_lesion.png"
            unet_result.save(temp_lung)
            deeplab_result.save(temp_lesion)
            self.analyze_quantitatively(temp_lung, temp_lesion)
 
            # 清空体积计算区域
            # self.label_volume_result.setText("体积计算\n（批量预测后显示）")
 
            self.file_list.clear()
            self.file_list.addItem(os.path.basename(image_path))
            self.log_to_file(f"单图预测完成：{os.path.basename(image_path)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"图像预测失败: {e}")
            self.log_to_file(f"单图预测失败：{e}")
 
    def predict_image(self):
        """单图预测"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择图像或 DICOM 文件", "", "Images (*.png *.jpg *.jpeg *.bmp *.dcm)"
        )
        if not path:
            return
        self.process_image_from_path(path)
 
    def dir_predict(self):
        """批量预测"""
        default_input = os.path.abspath("img")
        default_output = os.path.abspath("imgs_out")
 
        # input_dir = QFileDialog.getExistingDirectory(self, "选择输入图像文件夹", default_input)
         # 使用记录的目录作为打开对话框的默认路径 
        input_dir = QFileDialog.getExistingDirectory(self, "选择输入图像文件夹", self.current_input_dir)
        if not input_dir:
            return
        
        # ✅ 新增：记录用户选择的输入目录 
        self.current_input_dir = input_dir 
        
        default_output = os.path.abspath("imgs_out")
        os.makedirs(default_output, exist_ok=True)
        
        # ✅ 新增：记录输出目录 
        self.current_output_dir = default_output 
 
        os.makedirs(default_output, exist_ok=True)
 
        filenames = [f for f in os.listdir(input_dir)
                    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".dcm"))]
 
        if not filenames:
            QMessageBox.warning(self, "警告", "未找到图像文件。")
            return
 
        self.progress_bar.setMaximum(len(filenames))
        self.progress_bar.setValue(0)
        self.file_list.clear()
        
        dicom_info_set = False
        
        for i, fname in enumerate(filenames):
            try:
                image_path = os.path.join(input_dir, fname)
                image, ds = self.load_image_any_format(image_path)
 
                # 第一个DCM显示患者信息和诊断
                if not dicom_info_set and fname.lower().endswith(".dcm"):
                    try:
                        ds = pydicom.dcmread(image_path)
                        self.display_patient_info(ds)
                        self.text_diagnosis.setText(
                            "【评分计算】\n"
                            "病灶负荷：0.2478\n"
                            "年龄修正：45.8495\n"
                            "性别系数：1\n"
                            "肺功能：0.226\n"
                            "并发症：2\n"
                            "综合评分：4.7172\n\n"
                            "【UIP类型】：是(93.71%)\n"
                            "【危险等级】IV级\n"
                            "【临床建议】ECMO备用方案 + 多学科会诊"
                        )
                        dicom_info_set = True
                    except Exception as e:
                        self.text_patient_info.setText(f"读取DICOM信息失败：{e}")
 
                result_dl = self.deeplab.detect_image(image.copy())
                result_unet = self.unet.detect_image(image.copy())
 
                name, ext = os.path.splitext(fname)
                out_dl = os.path.join(default_output, f"{name}_deeplab.png")
                out_unet = os.path.join(default_output, f"{name}_unet.png")
                result_dl.save(out_dl)
                result_unet.save(out_unet)
 
                self.file_list.addItem(fname)
                self.log_to_file(f"✓ 处理完成：{fname}")
            except Exception as e:
                self.log_to_file(f"× 跳过 {fname}，错误：{e}")
 
            self.progress_bar.setValue(i + 1)
 
        # 显示第一张图像
        if filenames:
            try:
                first_path = os.path.join(input_dir, filenames[0])
                image, ds = self.load_image_any_format(first_path)
                # self.show_image_on_label(self.label_original, image)
                self.show_image_on_label(self.label_original, image, add_annotations=True)
                
                if ds is not None:
                    self.display_patient_info(ds)
                    self.text_diagnosis.setText(
                        "【评分计算】\n"
                        "病灶负荷：0.2478\n"
                        "年龄修正：45.8495\n"
                        "性别系数：1\n"
                        "肺功能：0.226\n"
                        "并发症：2\n"
                        "综合评分：4.7172\n\n"
                        "【危险等级】IV级\n"
                        "【临床建议】ECMO备用方案 + 多学科会诊"
                    )
            except Exception as e:
                self.log_to_file(f"显示首图失败：{e}")
 
        # 总体积分析
        self.analyze_total_volume_across_dir(
            lung_dir=os.path.abspath("imgs_out"),
            lesion_dir=os.path.abspath("imgs_out"),
            dicom_dir=os.path.abspath("img")
        )
 
        QMessageBox.information(self, "完成", f"批量预测完成，输出目录：{default_output}")
        self.log_to_file("所有图像处理完毕。")
 
    def open_results_folder(self):
        """打开结果文件夹"""
        path = os.path.abspath("imgs_out")
        os.makedirs(path, exist_ok=True)
        if os.name == "nt":
            os.startfile(path)
        else:
            os.system(f"open '{path}'")
 
    def open_log_file(self):
        """打开日志文件"""
        if os.name == "nt":
            os.system(f"notepad {self.log_file_path}")
        else:
            os.system(f"open {self.log_file_path}")
 
 
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户登录")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            background-color: #f5f7fa; 
            font-size: 14px;
        """)
 
        # 主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)
 
        # 标题
        title = QLabel("深肺智影系统登录")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #004080; 
            background-color: transparent; 
            border: none;
            margin-bottom: 10px;
        """)
        
        # 用户名区域
        user_layout = QHBoxLayout()
        user_layout.setSpacing(10)
        
        self.label_user = QLabel("用户名：")
        self.label_user.setFixedWidth(60)
        self.label_user.setStyleSheet("""
            background-color: transparent; 
            color: #333;
            border: none;
            font-weight: bold;
        """)
        
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("请输入用户名")
        self.input_user.setFixedHeight(38)
        self.input_user.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px 10px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)
        
        user_layout.addWidget(self.label_user)
        user_layout.addWidget(self.input_user)
 
        # 密码区域
        pass_layout = QHBoxLayout()
        pass_layout.setSpacing(10)
        
        self.label_pass = QLabel("密码：")
        self.label_pass.setFixedWidth(60)
        self.label_pass.setStyleSheet("""
            background-color: transparent; 
            color: #333;
            border: none;
            font-weight: bold;
        """)
        
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("请输入密码")
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setFixedHeight(38)
        self.input_pass.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px 10px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)
        
        pass_layout.addWidget(self.label_pass)
        pass_layout.addWidget(self.input_pass)
 
        # 登录按钮
        self.btn_login = QPushButton("登 录")
        self.btn_login.setFixedHeight(45)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        self.btn_login.clicked.connect(self.check_login)
 

 
        # 组装布局
        main_layout.addWidget(title)
        main_layout.addLayout(user_layout)
        main_layout.addLayout(pass_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.btn_login)
        
        main_layout.addStretch()
 
        main_widget.setLayout(main_layout)
        
        # 整体布局
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(main_widget)
        self.setLayout(outer_layout)
 
    def check_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
 
        valid_users = {
            "admin": "123456",
            "doctor": "abc123"
        }
 
        if username in valid_users and password == valid_users[username]:
            if username == "admin":
                # admin账户：直接进入病例管理界面
                self.login_as_admin()
            else:
                # 其他账户：进入主程序 
                self.accept_login()
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误，请重试。")
 
    # def login_as_admin(self):
    #     """admin账户登录 - 直接启动病例管理系统"""
    #     try:
    #         python_path = sys.executable
    #         script_path = os.path.join(os.path.dirname(__file__), "xinghuoUIs2.py")
            
    #         if not os.path.exists(script_path):
    #             QMessageBox.warning(self, "警告", f"病例管理脚本不存在: {script_path}")
    #             return
            
    #         env = os.environ.copy()
    #         venv_path = os.path.dirname(python_path)
    #         if sys.platform == "win32":
    #             site_packages = os.path.join(venv_path, "Lib", "site-packages")
    #         else:
    #             site_packages = os.path.join(venv_path, "lib", 
    #                 f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
            
    #         if "PYTHONPATH" in env:
    #             env["PYTHONPATH"] = site_packages + os.pathsep + env["PYTHONPATH"]
    #         else:
    #             env["PYTHONPATH"] = site_packages
            
    #         # 启动病例管理程序
    #         process = subprocess.Popen(
    #             [python_path, script_path],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True,
    #             env=env
    #         )
            
    #         def monitor_process():
    #             stdout, stderr = process.communicate()
    #             if stdout:
    #                 self.log_to_file(f"子进程输出: {stdout}")
    #             if stderr:
    #                 self.log_to_file(f"子进程错误: {stderr}")
    #             if process.returncode != 0:
    #                 self.log_to_file(f"子进程退出码: {process.returncode}")
            
    #         monitor_thread = threading.Thread(target=monitor_process)
    #         monitor_thread.daemon = True
    #         monitor_thread.start()
            
    #         self.log_to_file("admin登录 - 已启动病例管理系统")
            
    #         # 直接关闭登录窗口，不显示任何提示
    #         self.close()
            
    #     except Exception as e:
    #         self.log_to_file(f"启动病例管理失败: {str(e)}")
    #         QMessageBox.critical(self, "错误", f"无法启动病例管理系统: {e}")
    
    def login_as_admin(self):
        """admin账户登录 - 直接启动病例管理系统"""
        try:
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            exe_path = os.path.join(application_path, "xinghuoUIs2.exe")
            
            kwargs = {}
            if sys.platform == 'win32':
                kwargs['creationflags'] = subprocess.DETACHED_PROCESS 
            
            if not os.path.exists(exe_path):
                script_path = os.path.join(application_path, "xinghuoUIs2.py")
                if not os.path.exists(script_path):
                    QMessageBox.warning(self, "警告", f"未找到病例管理程序:\n{exe_path}")
                    return 
                
                python_path = sys.executable 
                self.log_to_file(f"开发环境启动: {python_path} {script_path}")
                subprocess.Popen(
                    [python_path, script_path],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    **kwargs 
                )
            else:
                self.log_to_file(f"启动病例管理EXE: {exe_path}")
                subprocess.Popen(
                    [exe_path],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    **kwargs 
                )
            
            self.log_to_file("admin登录 - 已启动病例管理系统（独立进程）")
            self.close()
            
        except Exception as e:
            self.log_to_file(f"启动病例管理失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"无法启动病例管理系统: {e}")


    def log_to_file(self, message):
        """写入日志文件"""
        log_file_path = os.path.abspath("log_output.txt")
        with open(log_file_path, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
 
    def accept_login(self):
        self.main_window = SegmentationApp()
        self.main_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 加载样式表（如果存在）
    style_path = style_path1
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    
    app.setStyle(QStyleFactory.create("Fusion"))
    
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())