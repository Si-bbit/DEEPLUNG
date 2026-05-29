import sys
import os
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QListWidgetItem,
    QComboBox, QCheckBox, QFileDialog, QGroupBox, QTabWidget, QProgressBar,
    QTableWidget, QTableWidgetItem, QHeaderView, QStatusBar, QMessageBox,
    QFrame, QSplitter, QScrollArea
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette
from PySide6.QtCore import Qt, QTimer, Signal, QThread
 
 
class AdminWindow(QMainWindow):
    """管理员设置界面"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("系统管理 - 深肺智影")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(900, 600)
        
        # 样式设置
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #0078d4;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
            QPushButton#btn_danger {
                background-color: #dc3545;
            }
            QPushButton#btn_danger:hover {
                background-color: #c82333;
            }
            QPushButton#btn_success {
                background-color: #28a745;
            }
            QPushButton#btn_success:hover {
                background-color: #218838;
            }
            QPushButton#btn_warning {
                background-color: #ffc107;
                color: #333;
            }
            QPushButton#btn_warning:hover {
                background-color: #e0a800;
            }
            QLineEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #0078d4;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
            QTableWidget {
                border: 1px solid #ccc;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QHeaderView::section {
                background-color: #e8f4fc;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #333;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #28a745;
            }
            QLabel#title_label {
                font-size: 24px;
                font-weight: bold;
                color: #004080;
            }
            QLabel#status_ok {
                color: #28a745;
                font-weight: bold;
            }
            QLabel#status_error {
                color: #dc3545;
                font-weight: bold;
            }
            QLabel#status_warning {
                color: #ffc107;
                font-weight: bold;
            }
        """)
        
        self.init_ui()
        self.log_message("系统管理界面已启动")
    
    def init_ui(self):
        """初始化界面"""
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        central_widget.setLayout(main_layout)
        
        # 标题
        title_label = QLabel("⚙️ 系统管理")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建TabWidget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e8f4fc;
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #0078d4;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #d0e8f8;
            }
        """)
        
        # 创建三个标签页
        self.tab_model = self.create_model_management_tab()
        self.tab_config = self.create_config_tab()
        self.tab_log = self.create_log_tab()
        self.tab_user = self.create_user_management_tab()
 
        self.tabs.addTab(self.tab_model, "模型管理")
        self.tabs.addTab(self.tab_config, "运行配置")
        self.tabs.addTab(self.tab_log, "系统日志")
        # 新增用户管理标签页
        self.tabs.addTab(self.tab_user, "用户管理")
        # self.tabs.addTab(self.tab_model, "🤖 模型管理")
        # self.tabs.addTab(self.tab_config, "⚡ 运行配置")
        # self.tabs.addTab(self.tab_log, "📋 系统日志")
        
        main_layout.addWidget(self.tabs)
        
        # 底部状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
    
    # ==================== 模型管理模块 ====================
    
    def create_model_management_tab(self):
        """创建模型管理标签页 - 支持双模型选择"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        widget.setLayout(layout)
        
        # ==================== 肺实质分割模型 ====================
        lung_group = QGroupBox("肺实质分割模型")
        lung_layout = QVBoxLayout()
        lung_layout.setSpacing(10)
        
        # 肺实质模型表格
        self.lung_model_table = QTableWidget()
        self.lung_model_table.setColumnCount(4)
        self.lung_model_table.setHorizontalHeaderLabels(["模型名称", "模型类型", "权重文件路径", "操作"])
        self.lung_model_table.horizontalHeader().setStretchLastSection(True)
        self.lung_model_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.lung_model_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lung_model_table.setRowCount(2)
        
        # 模拟肺实质模型数据
        lung_models = [
            ("AG-ResUNet-Lung", "分割模型", "pths/deeplab_lung.pth", "✓ 已选中"),
            ("ResUNet-Lung", "分割模型", "pths/unet_lung.pth", "选择"),
        ]
        for row, (name, mtype, path, action_text) in enumerate(lung_models):
            self.lung_model_table.setItem(row, 0, QTableWidgetItem(name))
            self.lung_model_table.setItem(row, 1, QTableWidgetItem(mtype))
            self.lung_model_table.setItem(row, 2, QTableWidgetItem(path))
            action_item = QTableWidgetItem(action_text)
            action_item.setTextAlignment(Qt.AlignCenter)
            self.lung_model_table.setItem(row, 3, action_item)
        
        self.lung_model_table.cellClicked.connect(self.on_lung_model_clicked)
        lung_layout.addWidget(self.lung_model_table)
        
        # 肺实质模型操作按钮
# 肺实质模型操作按钮
        lung_btn_layout = QHBoxLayout()
        lung_btn_layout.setSpacing(10)
        
        btn_add_lung = QPushButton("➕ 添加模型")
        btn_add_lung.clicked.connect(lambda: self.add_model("lung"))
        
        btn_replace_lung = QPushButton("🔄 替换模型")
        btn_replace_lung.clicked.connect(lambda: self.replace_model("lung"))
 
# ========== 修改刷新按钮样式 ==========
        btn_refresh_lung = QPushButton("🔃 刷新")
        btn_refresh_lung.setObjectName("btn_refresh")
        btn_refresh_lung.setStyleSheet("""
            QPushButton#btn_refresh {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QPushButton#btn_refresh:hover {
                background-color: #f0f0f0;
                border: 1px solid #999999;
            }
            QPushButton#btn_refresh:pressed {
                background-color: #e0e0e0;
            }
        """)
        # =======================================
        
        btn_refresh_lung.clicked.connect(lambda: self.refresh_models("lung"))
        
        lung_btn_layout.addWidget(btn_add_lung)
        lung_btn_layout.addWidget(btn_replace_lung)
        lung_btn_layout.addStretch()
        lung_btn_layout.addWidget(btn_refresh_lung)
        lung_layout.addLayout(lung_btn_layout)
        
        lung_group.setLayout(lung_layout)
        layout.addWidget(lung_group)
        
        # ==================== 病灶分割模型 ====================
        lesion_group = QGroupBox("病灶分割模型")
        lesion_layout = QVBoxLayout()
        lesion_layout.setSpacing(10)
        
        # 病灶模型表格
        self.lesion_model_table = QTableWidget()
        self.lesion_model_table.setColumnCount(4)
        self.lesion_model_table.setHorizontalHeaderLabels(["模型名称", "模型类型", "权重文件路径", "操作"])
        self.lesion_model_table.horizontalHeader().setStretchLastSection(True)
        self.lesion_model_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.lesion_model_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lesion_model_table.setRowCount(2)
        
        # 模拟病灶模型数据
        lesion_models = [
            ("Deeplabv3plus-Lesion", "分割模型", "pths/unet_lesion.pth", "✓ 已选中"),
            ("nnUNet-Lesion", "分割模型", "pths/resunet_lesion.pth", "选择"),
        ]
        for row, (name, mtype, path, action_text) in enumerate(lesion_models):
            self.lesion_model_table.setItem(row, 0, QTableWidgetItem(name))
            self.lesion_model_table.setItem(row, 1, QTableWidgetItem(mtype))
            self.lesion_model_table.setItem(row, 2, QTableWidgetItem(path))
            action_item = QTableWidgetItem(action_text)
            action_item.setTextAlignment(Qt.AlignCenter)
            self.lesion_model_table.setItem(row, 3, action_item)
        
        self.lesion_model_table.cellClicked.connect(self.on_lesion_model_clicked)
        lesion_layout.addWidget(self.lesion_model_table)
        
        # 病灶模型操作按钮
        # 病灶模型操作按钮
        lesion_btn_layout = QHBoxLayout()
        lesion_btn_layout.setSpacing(10)
        
        btn_add_lesion = QPushButton("➕ 添加模型")
        btn_add_lesion.clicked.connect(lambda: self.add_model("lesion"))
        
        btn_replace_lesion = QPushButton("🔄 替换模型")
        btn_replace_lesion.clicked.connect(lambda: self.replace_model("lesion"))
        
# ========== 修改刷新按钮样式 ==========
        btn_refresh_lesion = QPushButton("🔃 刷新")
        btn_refresh_lesion.setObjectName("btn_refresh")
        btn_refresh_lesion.setStyleSheet("""
            QPushButton#btn_refresh {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QPushButton#btn_refresh:hover {
                background-color: #f0f0f0;
                border: 1px solid #999999;
            }
            QPushButton#btn_refresh:pressed {
                background-color: #e0e0e0;
            }
        """)
        # =======================================
        
        btn_refresh_lesion.clicked.connect(lambda: self.refresh_models("lesion"))
        
        lesion_btn_layout.addWidget(btn_add_lesion)
        lesion_btn_layout.addWidget(btn_replace_lesion)
        lesion_btn_layout.addStretch()
        lesion_btn_layout.addWidget(btn_refresh_lesion)
        lesion_layout.addLayout(lesion_btn_layout)
        
        lesion_group.setLayout(lesion_layout)
        layout.addWidget(lesion_group)
        
        # ==================== 当前选中模型状态 ====================
        status_group = QGroupBox("当前选中的模型")
        status_layout = QHBoxLayout()
        status_layout.setSpacing(30)
        
        # 肺实质模型状态
        lung_status_widget = QFrame()
        lung_status_widget.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        lung_status_widget.setStyleSheet("""
            QFrame {
                background-color: #e8f5e9;
                border: 2px solid #4caf50;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        lung_status_layout = QVBoxLayout()
        lung_status_layout.addWidget(QLabel("肺实质分割"))
        self.lung_selected_label = QLabel("DeepLabV3-Lung")
        self.lung_selected_label.setStyleSheet("font-weight: bold; color: #2e7d32; font-size: 14px;")
        lung_status_layout.addWidget(self.lung_selected_label)
        lung_status_widget.setLayout(lung_status_layout)
        status_layout.addWidget(lung_status_widget)
        
        # 病灶模型状态
        lesion_status_widget = QFrame()
        lesion_status_widget.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        lesion_status_widget.setStyleSheet("""
            QFrame {
                background-color: #ffebee;
                border: 2px solid #f44336;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        lesion_status_layout = QVBoxLayout()
        lesion_status_layout.addWidget(QLabel("病灶分割"))
        self.lesion_selected_label = QLabel("UNet-Lesion")
        self.lesion_selected_label.setStyleSheet("font-weight: bold; color: #c62828; font-size: 14px;")
        lesion_status_layout.addWidget(self.lesion_selected_label)
        lesion_status_widget.setLayout(lesion_status_layout)
        status_layout.addWidget(lesion_status_widget)
        
        status_layout.addStretch()
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 提示信息
        info_label = QLabel("💡 提示：点击表格中的「选择」按钮可切换当前使用的模型。两种模型可独立选择，分别用于肺实质和病灶的分割任务。")
        info_label.setStyleSheet("color: #666; font-size: 12px; background-color: transparent; border: none;")
        layout.addWidget(info_label)
        
        return widget
    
    
    def on_lung_model_clicked(self, row, column):
        """肺实质模型表格点击事件"""
        if column == 3:  # 操作列 
            action_text = self.lung_model_table.item(row, 3).text()
            if "选择" in action_text:
                self.select_lung_model(row)
    
    
    def on_lesion_model_clicked(self, row, column):
        """病灶模型表格点击事件"""
        if column == 3:  # 操作列
            action_text = self.lesion_model_table.item(row, 3).text()
            if "选择" in action_text:
                self.select_lesion_model(row)
    
    
    def select_lung_model(self, row):
        """选择肺实质分割模型"""
        model_name = self.lung_model_table.item(row, 0).text()
        model_path = self.lung_model_table.item(row, 2).text()
        
        # 更新表格状态
        for r in range(self.lung_model_table.rowCount()):
            if r == row:
                self.lung_model_table.setItem(r, 3, QTableWidgetItem("✓ 已选中"))
                self.lung_model_table.item(r, 3).setTextAlignment(Qt.AlignCenter)
            else:
                self.lung_model_table.setItem(r, 3, QTableWidgetItem("选择"))
                self.lung_model_table.item(r, 3).setTextAlignment(Qt.AlignCenter)
        
        # 更新状态显示
        self.lung_selected_label.setText(model_name)
        
        self.log_message(f"已选择肺实质分割模型: {model_name} ({model_path})")
        QMessageBox.information(self, "选择成功", f"肺实质分割模型已切换为: {model_name}")
    
    
    def select_lesion_model(self, row):
        """选择病灶分割模型"""
        model_name = self.lesion_model_table.item(row, 0).text()
        model_path = self.lesion_model_table.item(row, 2).text()
        
        # 更新表格状态
        for r in range(self.lesion_model_table.rowCount()):
            if r == row:
                self.lesion_model_table.setItem(r, 3, QTableWidgetItem("✓ 已选中"))
                self.lesion_model_table.item(r, 3).setTextAlignment(Qt.AlignCenter)
            else:
                self.lesion_model_table.setItem(r, 3, QTableWidgetItem("选择"))
                self.lesion_model_table.item(r, 3).setTextAlignment(Qt.AlignCenter)
        
        # 更新状态显示
        self.lesion_selected_label.setText(model_name)
        
        self.log_message(f"已选择病灶分割模型: {model_name} ({model_path})")
        QMessageBox.information(self, "选择成功", f"病灶分割模型已切换为: {model_name}")
    
    
    def add_model(self, model_type):
        """添加模型"""
        model_name = "肺实质分割" if model_type == "lung" else "病灶分割"
        file_path, _ = QFileDialog.getOpenFileName(
            self, f"选择{model_name}模型文件", "",
            "模型文件 (*.pth *.h5 *.onnx *.pt);;所有文件 (*)"
        )
        if file_path:
            self.log_message(f"添加{model_name}模型: {file_path}")
            QMessageBox.information(self, "成功", f"模型已添加: {os.path.basename(file_path)}")
    
    
    def replace_model(self, model_type):
        """替换模型"""
        model_name = "肺实质分割" if model_type == "lung" else "病灶分割"
        table = self.lung_model_table if model_type == "lung" else self.lesion_model_table
        current_row = table.currentRow()
        
        if current_row >= 0:
            current_model = table.item(current_row, 0).text()
            file_path, _ = QFileDialog.getOpenFileName(
                self, f"替换{model_name}模型 - {current_model}", "",
                "模型文件 (*.pth *.h5 *.onnx *.pt);;所有文件 (*)"
            )
            if file_path:
                table.setItem(current_row, 2, QTableWidgetItem(file_path))
                self.log_message(f"替换{model_name}模型: {file_path}")
                QMessageBox.information(self, "成功", f"模型已替换: {os.path.basename(file_path)}")
        else:
            QMessageBox.warning(self, "警告", "请先选择要替换的模型")
    
    
    def refresh_models(self, model_type):
        """刷新模型列表"""
        model_name = "肺实质分割" if model_type == "lung" else "病灶分割"
        self.log_message(f"正在刷新{model_name}模型列表...")
        QMessageBox.information(self, "刷新完成", f"{model_name}模型列表已刷新")


    def on_model_action_clicked(self, row, column):
        """模型表格点击事件"""
        if column == 4:  # 操作列
            action_text = self.model_table.item(row, 4).text()
            if action_text == "设为默认":
                self.set_default_model(row)
            elif action_text == "删除":
                self.delete_model()
    
    def set_default_model(self, row):
        """设置默认模型"""
        model_name = self.model_table.item(row, 0).text()
        for r in range(self.model_table.rowCount()):
            if r == row:
                self.model_table.setItem(r, 3, QTableWidgetItem("✓ 默认"))
                self.model_table.item(r, 3).setTextAlignment(Qt.AlignCenter)
                self.model_table.setItem(r, 4, QTableWidgetItem("当前默认"))
            else:
                self.model_table.setItem(r, 3, QTableWidgetItem("○"))
                self.model_table.item(r, 3).setTextAlignment(Qt.AlignCenter)
                self.model_table.setItem(r, 4, QTableWidgetItem("设为默认"))
        self.log_message(f"已将默认模型设置为: {model_name}")
        QMessageBox.information(self, "设置成功", f"已将默认模型设置为: {model_name}")
    
    def add_model(self):
        """添加模型"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择模型文件", "", 
            "模型文件 (*.pth *.h5 *.onnx *.pt);;所有文件 (*)"
        )
        if file_path:
            self.log_message(f"添加模型: {file_path}")
            QMessageBox.information(self, "成功", f"模型已添加: {os.path.basename(file_path)}")
    
    def replace_model(self):
        """替换模型"""
        current_row = self.model_table.currentRow()
        if current_row >= 0:
            model_name = self.model_table.item(current_row, 0).text()
            file_path, _ = QFileDialog.getOpenFileName(
                self, f"替换模型 - {model_name}", "",
                "模型文件 (*.pth *.h5 *.onnx *.pt);;所有文件 (*)"
            )
            if file_path:
                self.model_table.setItem(current_row, 2, QTableWidgetItem(file_path))
                self.log_message(f"替换模型 {model_name}: {file_path}")
                QMessageBox.information(self, "成功", f"模型已替换: {os.path.basename(file_path)}")
        else:
            QMessageBox.warning(self, "警告", "请先选择要替换的模型")
    
    def delete_model(self):
        """删除模型"""
        current_row = self.model_table.currentRow()
        if current_row >= 0:
            model_name = self.model_table.item(current_row, 0).text()
            reply = QMessageBox.question(
                self, "确认删除", 
                f"确定要删除模型「{model_name}」吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.model_table.removeRow(current_row)
                self.log_message(f"删除模型: {model_name}")
        else:
            QMessageBox.warning(self, "警告", "请先选择要删除的模型")
    
    def refresh_models(self):
        """刷新模型列表"""
        self.log_message("正在刷新模型列表...")
        # 实际应用中这里会重新扫描模型目录
        QMessageBox.information(self, "刷新完成", "模型列表已刷新")
    
    # ==================== 运行参数配置模块 ====================
    
    def create_config_tab(self):
        """创建运行配置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        widget.setLayout(layout)
        
        # 推理设备配置
        device_group = QGroupBox("🖥 推理设备配置")
        device_layout = QGridLayout()
        device_layout.setSpacing(15)
        
        # 设备选择
        device_layout.addWidget(QLabel("推理设备："), 0, 0)
        self.combo_device = QComboBox()
        self.combo_device.addItems(["CPU", "GPU 0 (CUDA)", "GPU 1 (CUDA)", "GPU 2 (CUDA)"])
        self.combo_device.setCurrentIndex(1)  # 默认GPU
        device_layout.addWidget(self.combo_device, 0, 1)
        
        # GPU显存设置
        device_layout.addWidget(QLabel("GPU显存限制："), 0, 2)
        self.combo_gpu_memory = QComboBox()
        self.combo_gpu_memory.addItems(["2GB", "4GB", "6GB", "8GB", "无限制"])
        self.combo_gpu_memory.setCurrentIndex(3)
        device_layout.addWidget(self.combo_gpu_memory, 0, 3)
        
        # 批处理大小
        device_layout.addWidget(QLabel("批处理大小："), 1, 0)
        self.spin_batch = QLineEdit("4")
        self.spin_batch.setPlaceholderText("1-32")
        device_layout.addWidget(self.spin_batch, 1, 1)
        
        # 线程数
        device_layout.addWidget(QLabel("CPU线程数："), 1, 2)
        self.spin_threads = QLineEdit("8")
        self.spin_threads.setPlaceholderText("1-32")
        device_layout.addWidget(self.spin_threads, 1, 3)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # 路径配置
        path_group = QGroupBox("路径配置")
        path_layout = QGridLayout()
        path_layout.setSpacing(15)
        
        # 输入目录
        path_layout.addWidget(QLabel("输入图像目录："), 0, 0)
        self.edit_input_path = QLineEdit("./img")
        path_layout.addWidget(self.edit_input_path, 0, 1)
        btn_input_browse = QPushButton("浏览")
        btn_input_browse.setFixedWidth(80)
        btn_input_browse.clicked.connect(lambda: self.browse_folder(self.edit_input_path))
        path_layout.addWidget(btn_input_browse, 0, 2)
        
        # 输出目录
        path_layout.addWidget(QLabel("输出结果目录："), 1, 0)
        self.edit_output_path = QLineEdit("./imgs_out")
        path_layout.addWidget(self.edit_output_path, 1, 1)
        btn_output_browse = QPushButton("浏览")
        btn_output_browse.setFixedWidth(80)
        btn_output_browse.clicked.connect(lambda: self.browse_folder(self.edit_output_path))
        path_layout.addWidget(btn_output_browse, 1, 2)
        
        # 模型目录
        path_layout.addWidget(QLabel("模型权重目录："), 2, 0)
        self.edit_model_path = QLineEdit("./logs")
        path_layout.addWidget(self.edit_model_path, 2, 1)
        btn_model_browse = QPushButton("浏览")
        btn_model_browse.setFixedWidth(80)
        btn_model_browse.clicked.connect(lambda: self.browse_folder(self.edit_model_path))
        path_layout.addWidget(btn_model_browse, 2, 2)
        
        # 日志目录
        path_layout.addWidget(QLabel("日志文件目录："), 3, 0)
        self.edit_log_path = QLineEdit("./")
        path_layout.addWidget(self.edit_log_path, 3, 1)
        btn_log_browse = QPushButton("浏览")
        btn_log_browse.setFixedWidth(80)
        btn_log_browse.clicked.connect(lambda: self.browse_folder(self.edit_log_path))
        path_layout.addWidget(btn_log_browse, 3, 2)
        
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)
        
        # 推理选项配置
        options_group = QGroupBox("推理选项")
        options_layout = QGridLayout()
        options_layout.setSpacing(15)
        
        # 复选框选项
        self.check_auto_save = QCheckBox("自动保存分割结果")
        self.check_auto_save.setChecked(True)
        options_layout.addWidget(self.check_auto_save, 0, 0)
        
        self.check_show_progress = QCheckBox("显示推理进度")
        self.check_show_progress.setChecked(True)
        options_layout.addWidget(self.check_show_progress, 0, 1)
        
        self.check_verbose = QCheckBox("详细输出模式")
        options_layout.addWidget(self.check_verbose, 0, 2)
        
        self.check_cudnn_benchmark = QCheckBox("启用CuDNN加速")
        self.check_cudnn_benchmark.setChecked(True)
        options_layout.addWidget(self.check_cudnn_benchmark, 1, 0)
        
        self.check_fp16 = QCheckBox("混合精度推理(FP16)")
        options_layout.addWidget(self.check_fp16, 1, 1)
        
        self.check_multiprocess = QCheckBox("多进程数据加载")
        options_layout.addWidget(self.check_multiprocess, 1, 2)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 保存配置按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_save = QPushButton("💾 保存配置")
        btn_save.setObjectName("btn_success")
        btn_save.clicked.connect(self.save_config)
        btn_layout.addWidget(btn_save)
        
        btn_reset = QPushButton("🔄 重置默认")
        btn_reset.setObjectName("btn_warning")
        btn_reset.clicked.connect(self.reset_config)
        btn_layout.addWidget(btn_reset)
        
        layout.addLayout(btn_layout)
        
        return widget 
    
    def browse_folder(self, line_edit):
        """浏览文件夹"""
        directory = QFileDialog.getExistingDirectory(self, "选择目录", line_edit.text())
        if directory:
            line_edit.setText(directory)
    
    def save_config(self):
        """保存配置"""
        config = {
            "device": self.combo_device.currentText(),
            "gpu_memory": self.combo_gpu_memory.currentText(),
            "batch_size": self.spin_batch.text(),
            "cpu_threads": self.spin_threads.text(),
            "input_path": self.edit_input_path.text(),
            "output_path": self.edit_output_path.text(),
            "model_path": self.edit_model_path.text(),
            "log_path": self.edit_log_path.text(),
            "auto_save": self.check_auto_save.isChecked(),
            "show_progress": self.check_show_progress.isChecked(),
            "verbose": self.check_verbose.isChecked(),
            "cudnn_benchmark": self.check_cudnn_benchmark.isChecked(),
            "fp16": self.check_fp16.isChecked(),
            "multiprocess": self.check_multiprocess.isChecked(),
        }
        self.log_message(f"配置已保存: 设备={config['device']}, 批大小={config['batch_size']}")
        QMessageBox.information(self, "保存成功", "运行配置已保存")
    
    def reset_config(self):
        """重置配置"""
        reply = QMessageBox.question(
            self, "确认重置", "确定要重置为默认配置吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.combo_device.setCurrentIndex(1)
            self.combo_gpu_memory.setCurrentIndex(3)
            self.spin_batch.setText("4")
            self.spin_threads.setText("8")
            self.edit_input_path.setText("./img")
            self.edit_output_path.setText("./imgs_out")
            self.edit_model_path.setText("./logs")
            self.edit_log_path.setText("./")
            self.check_auto_save.setChecked(True)
            self.check_show_progress.setChecked(True)
            self.check_verbose.setChecked(False)
            self.check_cudnn_benchmark.setChecked(True)
            self.check_fp16.setChecked(False)
            self.check_multiprocess.setChecked(False)
            self.log_message("配置已重置为默认值")
            QMessageBox.information(self, "重置完成", "配置已重置为默认值")
    
    # ==================== 系统日志模块 ====================
    
    def create_log_tab(self):
        """创建系统日志标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        widget.setLayout(layout)
        
        # 状态概览
        status_group = QGroupBox("📊 系统状态概览")
        status_layout = QGridLayout()
        status_layout.setSpacing(20)
        
        # 状态指示器
        self.label_gpu_status = QLabel("🟢 GPU状态: 正常")
        self.label_gpu_status.setObjectName("status_ok")
        
        self.label_model_status = QLabel("🟢 模型状态: 已加载")
        self.label_model_status.setObjectName("status_ok")
        
        self.label_memory_status = QLabel("🟢 内存状态: 正常 (使用 3.2GB/16GB)")
        self.label_memory_status.setObjectName("status_ok")
        
        self.label_disk_status = QLabel("🟢 磁盘状态: 充足 (可用 256GB)")
        self.label_disk_status.setObjectName("status_ok")
        
        status_layout.addWidget(self.label_gpu_status, 0, 0)
        status_layout.addWidget(self.label_model_status, 0, 1)
        status_layout.addWidget(self.label_memory_status, 1, 0)
        status_layout.addWidget(self.label_disk_status, 1, 1)
        
        # 性能指标
        perf_label = QLabel("📈 推理性能指标")
        perf_label.setStyleSheet("font-weight: bold; color: #333;")
        status_layout.addWidget(perf_label, 2, 0, 1, 2)
        
        status_layout.addWidget(QLabel("今日推理次数:"), 3, 0)
        self.label_infer_count = QLabel("156 次")
        self.label_infer_count.setStyleSheet("font-weight: bold; color: #0078d4;")
        status_layout.addWidget(self.label_infer_count, 3, 1)
        
        status_layout.addWidget(QLabel("平均推理时间:"), 4, 0)
        self.label_avg_time = QLabel("2.35 秒/张")
        self.label_avg_time.setStyleSheet("font-weight: bold; color: #0078d4;")
        status_layout.addWidget(self.label_avg_time, 4, 1)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 日志显示区域
        log_group = QGroupBox("📋 运行日志")
        log_layout = QVBoxLayout()
        
        # 日志过滤器
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        filter_layout.addWidget(QLabel("日志级别:"))
        self.combo_log_level = QComboBox()
        self.combo_log_level.addItems(["全部", "INFO", "WARNING", "ERROR"])
        self.combo_log_level.setCurrentIndex(0)
        filter_layout.addWidget(self.combo_log_level)
        
        filter_layout.addWidget(QLabel("搜索:"))
        self.edit_log_search = QLineEdit()
        self.edit_log_search.setPlaceholderText("输入关键词搜索...")
        self.edit_log_search.setFixedWidth(200)
        filter_layout.addWidget(self.edit_log_search)
        
        filter_layout.addStretch()
        
        btn_clear = QPushButton("清空日志")
        btn_clear.clicked.connect(self.clear_log)
        filter_layout.addWidget(btn_clear)
        
        btn_export = QPushButton("导出日志")
        btn_export.clicked.connect(self.export_log)
        filter_layout.addWidget(btn_export)
        
        log_layout.addLayout(filter_layout)
        
        # 日志文本框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        
        # 添加一些示例日志
        self.log_text.append("[2026-01-15 09:23:15] INFO: 系统启动完成")
        self.log_text.append("[2026-01-15 09:23:16] INFO: 加载模型 DeepLabV3+ (logs/deeplab.pth)")
        self.log_text.append("[2026-01-15 09:23:18] INFO: 模型加载成功，推理设备: GPU 0")
        self.log_text.append("[2026-01-15 09:25:32] INFO: 开始推理: img001.dcm")
        self.log_text.append("[2026-01-15 09:25:34] INFO: 推理完成，耗时 2.31s")
        self.log_text.append("[2026-01-15 09:28:45] WARNING: GPU显存使用率达 78%")
        
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        return widget
    
    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] INFO: {message}"
        self.log_text.append(log_entry)
        
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # 更新状态栏
        self.statusBar.showMessage(message, 3000)
    
    def clear_log(self):
        """清空日志"""
        reply = QMessageBox.question(
            self, "确认清空", "确定要清空所有日志吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.log_text.clear()
            self.log_message("日志已清空")
    
    def export_log(self):
        """导出日志"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出日志", 
            f"system_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                QMessageBox.information(self, "导出成功", f"日志已导出到: {file_path}")
                self.log_message(f"日志已导出: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"无法保存文件: {e}")
 
    def create_user_management_tab(self):
        """创建用户管理标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        widget.setLayout(layout)
        
        # ==================== 用户列表 ====================
        user_group = QGroupBox("👥 用户列表")
        user_layout = QVBoxLayout()
        
        # 用户表格
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["用户名", "用户类型", "账号状态", "最后登录时间", "操作"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.setRowCount(4)
        
        # 模拟用户数据
        users = [
            ("admin", "管理员", "正常", "2026-01-15 09:00:00", "修改"),
            ("doctor1", "普通用户", "正常", "2026-01-14 15:30:00", "删除"),
            ("doctor2", "普通用户", "正常", "2026-01-13 10:20:00", "删除"),
            
        ]
        
        for row, (username, user_type, status, last_login, action) in enumerate(users):
            self.user_table.setItem(row, 0, QTableWidgetItem(username))
            
            # 用户类型
            type_item = QTableWidgetItem(user_type)
            if user_type == "管理员":
                type_item.setBackground(QColor("#e3f2fd"))
            else:
                type_item.setBackground(QColor("#f5f5f5"))
            self.user_table.setItem(row, 1, type_item)
            
            # 账号状态
            status_item = QTableWidgetItem(status)
            if status == "正常":
                status_item.setForeground(QColor("#4caf50"))
                status_item.setBackground(QColor("#e8f5e9"))
            else:
                status_item.setForeground(QColor("#f44336"))
                status_item.setBackground(QColor("#ffebee"))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 2, status_item)
            
            # 最后登录时间
            self.user_table.setItem(row, 3, QTableWidgetItem(last_login))
            
            # 操作
            action_item = QTableWidgetItem(action)
            action_item.setTextAlignment(Qt.AlignCenter)
            action_item.setForeground(QColor("#0078d4"))
            self.user_table.setItem(row, 4, action_item)
        
        self.user_table.cellClicked.connect(self.on_user_action_clicked)
        user_layout.addWidget(self.user_table)
        
        # 用户列表操作按钮
        user_btn_layout = QHBoxLayout()
        user_btn_layout.setSpacing(10)
        
        btn_refresh_user = QPushButton("🔃 刷新列表")
        btn_refresh_user.setObjectName("btn_refresh")
        btn_refresh_user.setStyleSheet("""
            QPushButton#btn_refresh {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QPushButton#btn_refresh:hover {
                background-color: #f0f0f0;
                border: 1px solid #999999;
            }
        """)
        btn_refresh_user.clicked.connect(self.refresh_user_list)
        
        user_btn_layout.addStretch()
        user_btn_layout.addWidget(btn_refresh_user)
        user_layout.addLayout(user_btn_layout)
        
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)
        
        # ==================== 添加用户 ====================
        add_group = QGroupBox("➕ 添加新用户")
        add_layout = QGridLayout()
        add_layout.setSpacing(15)
        add_layout.setColumnMinimumWidth(2, 20)
        
        # 用户名
        add_layout.addWidget(QLabel("用户名："), 0, 0)
        self.edit_new_username = QLineEdit()
        self.edit_new_username.setPlaceholderText("请输入用户名")
        self.edit_new_username.setFixedHeight(35)
        add_layout.addWidget(self.edit_new_username, 0, 1)
        
        # 密码
        add_layout.addWidget(QLabel("密码："), 0, 3)
        self.edit_new_password = QLineEdit()
        self.edit_new_password.setPlaceholderText("请输入密码")
        self.edit_new_password.setEchoMode(QLineEdit.Password)
        self.edit_new_password.setFixedHeight(35)
        add_layout.addWidget(self.edit_new_password, 0, 4)
        
        # 用户类型
        add_layout.addWidget(QLabel("用户类型："), 1, 0)
        self.combo_user_type = QComboBox()
        self.combo_user_type.addItems(["普通用户", "管理员"])
        self.combo_user_type.setFixedHeight(35)
        add_layout.addWidget(self.combo_user_type, 1, 1)
        
        # 账号状态
        add_layout.addWidget(QLabel("账号状态："), 1, 3)
        self.combo_user_status = QComboBox()
        self.combo_user_status.addItems(["正常", "已禁用"])
        self.combo_user_status.setFixedHeight(35)
        add_layout.addWidget(self.combo_user_status, 1, 4)
        
        # 添加按钮
        btn_add_user = QPushButton("➕ 添加用户")
        btn_add_user.setObjectName("btn_success")
        btn_add_user.setFixedHeight(40)
        btn_add_user.clicked.connect(self.add_new_user)
        add_layout.addWidget(btn_add_user, 2, 0, 1, 5)
        
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)
        
        # ==================== 用户统计 ====================
        stats_group = QGroupBox("📊 用户统计")
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        # 去掉医生统计框，只保留管理员和普通用户

        
        # 管理员数量
        admin_frame = QFrame()
        admin_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        admin_frame.setStyleSheet("""
            QFrame {
                background-color: #e3f2fd;
                border: 2px solid #2196f3;
                border-radius: 8px;
                padding: 15px;
                min-width: 120px;
            }
        """)
        admin_layout = QVBoxLayout()
        admin_layout.addWidget(QLabel("👤 管理员"))
        self.label_admin_count = QLabel("1 人")
        self.label_admin_count.setStyleSheet("font-weight: bold; color: #1565c0; font-size: 18px;")
        admin_layout.addWidget(self.label_admin_count)
        admin_frame.setLayout(admin_layout)
        stats_layout.addWidget(admin_frame)
        
        # 普通用户数量
        normal_frame = QFrame()
        normal_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        normal_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3e0;
                border: 2px solid #ff9800;
                border-radius: 8px;
                padding: 15px;
                min-width: 120px;
            }
        """)
        normal_layout = QVBoxLayout()
        normal_layout.addWidget(QLabel("👥 普通用户"))
        self.label_normal_count = QLabel("2 人")
        self.label_normal_count.setStyleSheet("font-weight: bold; color: #e65100; font-size: 18px;")
        normal_layout.addWidget(self.label_normal_count)
        normal_frame.setLayout(normal_layout)
        stats_layout.addWidget(normal_frame)
        
        stats_layout.addStretch()
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        return widget
    
    
    def on_user_action_clicked(self, row, column):
        """用户表格点击事件"""
        if column == 4:  # 操作列
            username = self.user_table.item(row, 0).text()
            action_text = self.user_table.item(row, 4).text()
            
            if action_text == "删除":
                self.delete_user(row)
            elif action_text == "修改":
                QMessageBox.information(self, "修改用户", f"修改用户: {username}")
    
    
    def delete_user(self, row):
        """删除用户"""
        username = self.user_table.item(row, 0).text()
        
        # 不允许删除管理员
        user_type = self.user_table.item(row, 1).text()
        if user_type == "管理员":
            QMessageBox.warning(self, "权限不足", "无法删除管理员账号")
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除用户「{username}」吗？\n此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.user_table.removeRow(row)
            self.log_message(f"删除用户: {username}")
            QMessageBox.information(self, "删除成功", f"用户「{username}」已删除")
    
    
    def refresh_user_list(self):
        """刷新用户列表"""
        self.log_message("正在刷新用户列表...")
        QMessageBox.information(self, "刷新完成", "用户列表已刷新")
    
    
    def add_new_user(self):
        """添加新用户（界面演示用）"""
        username = self.edit_new_username.text().strip()
        password = self.edit_new_password.text().strip()
        user_type = self.combo_user_type.currentText()
        status = self.combo_user_status.currentText()
        
        if not username or not password:
            QMessageBox.warning(self, "输入错误", "用户名和密码不能为空")
            return
        
        # 显示添加成功（演示用）
        QMessageBox.information(
            self, "添加成功", 
            f"用户「{username}」已添加！\n"
            f"用户类型：{user_type}\n"
            f"账号状态：{status}"
        )
        
        # 清空输入框
        self.edit_new_username.clear()
        self.edit_new_password.clear()
        self.combo_user_type.setCurrentIndex(0)
        self.combo_user_status.setCurrentIndex(0)
        
        self.log_message(f"添加新用户: {username} ({user_type})")
# 主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())