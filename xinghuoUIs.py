import sys 
import os
 
# 调试信息
print(f"Python路径: {sys.executable}")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', '未设置')}")
 
# 检查PySide6是否可导入 
try:
    import PySide6 
    print(f"PySide6版本: {PySide6.__version__}")
except ImportError as e:
    print(f"PySide6导入失败: {e}")
    # 打印模块搜索路径 
    print(f"模块搜索路径: {sys.path}")
    sys.exit(1)  # 退出并返回错误码 
 

import sys
import PySide6
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("病例管理")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建标签页
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)
        
       # 创建患者管理页面（修改版）
        patient_tab = QWidget()
        patient_layout = QVBoxLayout()
        patient_tab.setLayout(patient_layout)

        # 修改表头字段
        patient_table = QTableWidget()
        patient_table.setColumnCount(7)
        patient_table.setHorizontalHeaderLabels([
            '名字', 
            '性别', 
            '年龄', 
            'CT报告单日期', 
            '影像报告', 
            '诊断', 
            '检验时间'
        ])
        patient_layout.addWidget(patient_table)

        # 添加数据
        records = [
            ("患者1", "女", "73", "20220722", "机化性肺炎不除外，与2022-02-13CT对比大致相仿", "双肺间质性肺炎", "2022/7/21"),
            ("患者2", "男", "77", "20220407", "双肺间质改变、间质炎", "双肺细支气管炎", "2022/4/11"),
            ("患者3", "女", "79", "20220417", "双肺下叶间质炎改变", "肺气肿.", "2022/5/13"),
            ("患者4", "男", "50", "20211114", "右肺、左肺下叶多发磨玻璃斑片及实变影，考虑间质性炎症", "间质性炎症", "2021/11/10"),
            ("患者5", "男", "54", "20210827", "双肺间质性炎.细支气管炎", "双肺间质性炎", "2021/8/27"),
            ("患者6", "男", "72", "20210914", "肺气肿.双肺间质性改变", "肺气肿", "2021/9/21"),
        ]
        
        for row_idx, record in enumerate(records):
            patient_table.insertRow(row_idx)
            for col_idx, item in enumerate(record):
                patient_table.setItem(row_idx, col_idx, QTableWidgetItem(item))

        # 添加示例数据
        patient_table.insertRow(0)
        patient_table.setItem(0, 0, QTableWidgetItem("张三"))
        patient_table.setItem(0, 1, QTableWidgetItem("男"))  # 男
        patient_table.setItem(0, 2, QTableWidgetItem("43"))
        patient_table.setItem(0, 3, QTableWidgetItem("2025-05-01"))
        patient_table.setItem(0, 4, QTableWidgetItem("双肺基底节段网格影"))
        patient_table.setItem(0, 5, QTableWidgetItem("间质性肺炎"))
        patient_table.setItem(0, 6, QTableWidgetItem("2025-05-03"))

        patient_table.insertRow(1)
        patient_table.setItem(1, 0, QTableWidgetItem("李四"))
        patient_table.setItem(1, 1, QTableWidgetItem("女"))  # 无效数据
        patient_table.setItem(1, 2, QTableWidgetItem("58"))
        patient_table.setItem(1, 3, QTableWidgetItem("2025-04-25"))
        patient_table.setItem(1, 4, QTableWidgetItem("肺纹理增粗"))
        patient_table.setItem(1, 5, QTableWidgetItem("无明确诊断"))
        patient_table.setItem(1, 6, QTableWidgetItem("None"))

# （可选）移除原来的输入框和按钮，或者保留根据需要更新输入字段名称

        
        # 添加患者信息输入框和按钮
        patient_input_layout = QHBoxLayout()
        name_input = QLineEdit()
        age_input = QLineEdit()
        gender_input = QLineEdit()
        case_input = QLineEdit()
        add_button = QPushButton("查找患者")
        patient_input_layout.addWidget(QLabel("姓名:"))
        patient_input_layout.addWidget(name_input)
        patient_input_layout.addWidget(QLabel("年龄:"))
        patient_input_layout.addWidget(age_input)
        patient_input_layout.addWidget(QLabel("性别:"))
        patient_input_layout.addWidget(gender_input)
        patient_input_layout.addWidget(QLabel("病历号:"))
        patient_input_layout.addWidget(case_input)
        patient_input_layout.addWidget(add_button)
        patient_layout.addLayout(patient_input_layout)
        
        # 创建影像管理页面
        image_tab = QWidget()
        image_layout = QVBoxLayout()
        image_tab.setLayout(image_layout)
        
        # 添加影像信息表格
        image_table = QTableWidget()
        image_table.setColumnCount(3)
        image_table.setHorizontalHeaderLabels(['患者ID', '影像类型', '影像路径'])
        image_layout.addWidget(image_table)
        
        # 添加示例影像信息
        image_table.insertRow(0)
        image_table.setItem(0, 0, QTableWidgetItem("015000010"))
        image_table.setItem(0, 1, QTableWidgetItem("X光片"))
        image_table.setItem(0, 2, QTableWidgetItem("/images/xray1.jpg"))
        
        image_table.insertRow(1)
        image_table.setItem(1, 0, QTableWidgetItem("015000022"))
        image_table.setItem(1, 1, QTableWidgetItem("CT扫描"))
        image_table.setItem(1, 2, QTableWidgetItem("/images/ctscan2.jpg"))
        image_table.insertRow(2)
        image_table.setItem(2, 0, QTableWidgetItem("015001723"))
        image_table.setItem(2, 1, QTableWidgetItem("CT扫描"))
        image_table.setItem(2, 2, QTableWidgetItem("/images/ctscan2.jpg"))
        image_table.insertRow(3)
        image_table.setItem(3, 0, QTableWidgetItem("015000394"))
        image_table.setItem(3, 1, QTableWidgetItem("CT扫描"))
        image_table.setItem(3, 2, QTableWidgetItem("/images/ctscan2.jpg"))
        image_table.insertRow(4)
        image_table.setItem(4, 0, QTableWidgetItem("015000510"))
        image_table.setItem(4, 1, QTableWidgetItem("CT扫描"))
        image_table.setItem(4, 2, QTableWidgetItem("/images/ctscan2.jpg"))
        image_table.insertRow(5)
        image_table.setItem(5, 0, QTableWidgetItem("015009010"))
        image_table.setItem(5, 1, QTableWidgetItem("CT扫描"))
        image_table.setItem(5, 2, QTableWidgetItem("/images/ctscan2.jpg"))
        image_table.insertRow(6)
        image_table.setItem(6, 0, QTableWidgetItem("015068010"))
        image_table.setItem(6, 1, QTableWidgetItem("CT扫描"))
        image_table.setItem(6, 2, QTableWidgetItem("/images/ctscan2.jpg"))
        image_table.insertRow(7)
        image_table.setItem(7, 0, QTableWidgetItem("015006010"))
        image_table.setItem(7, 1, QTableWidgetItem("CT扫描"))
        image_table.setItem(7, 2, QTableWidgetItem("/images/ctscan2.jpg"))
        
        # 添加影像信息输入框和按钮
        image_input_layout = QHBoxLayout()
        patient_id_input = QLineEdit()
        image_type_input = QLineEdit()
        image_path_input = QLineEdit()
        add_image_button = QPushButton("添加影像")
        image_input_layout.addWidget(QLabel("患者ID:"))
        image_input_layout.addWidget(patient_id_input)
        image_input_layout.addWidget(QLabel("影像类型:"))
        image_input_layout.addWidget(image_type_input)
        image_input_layout.addWidget(QLabel("影像路径:"))
        image_input_layout.addWidget(image_path_input)
        image_input_layout.addWidget(add_image_button)
        image_layout.addLayout(image_input_layout)
        
        # 创建用户账号管理页面
        user_tab = QWidget()
        user_layout = QVBoxLayout()
        user_tab.setLayout(user_layout)
        
        # 添加用户账号表格
        user_table = QTableWidget()
        user_table.setColumnCount(3)
        user_table.setHorizontalHeaderLabels(['用户名', '密码', '角色'])
        user_layout.addWidget(user_table)
        
        # 添加示例用户账号信息
        user_table.insertRow(0)
        user_table.setItem(0, 0, QTableWidgetItem("admin"))
        user_table.setItem(0, 1, QTableWidgetItem("admin123"))
        user_table.setItem(0, 2, QTableWidgetItem("管理员"))
        
        user_table.insertRow(1)
        user_table.setItem(1, 0, QTableWidgetItem("doctor1"))
        user_table.setItem(1, 1, QTableWidgetItem("docpass123"))
        user_table.setItem(1, 2, QTableWidgetItem("普通用户"))
        
        # 添加用户账号输入框和按钮
        user_input_layout = QHBoxLayout()
        username_input = QLineEdit()
        password_input = QLineEdit()
        role_input = QLineEdit()
        add_user_button = QPushButton("添加用户")
        user_input_layout.addWidget(QLabel("用户名:"))
        user_input_layout.addWidget(username_input)
        user_input_layout.addWidget(QLabel("密码:"))
        user_input_layout.addWidget(password_input)
        user_input_layout.addWidget(QLabel("角色:"))
        user_input_layout.addWidget(role_input)
        user_input_layout.addWidget(add_user_button)
        user_layout.addLayout(user_input_layout)
        
        # 将三个页面添加到标签页中
        tab_widget.addTab(patient_tab, "患者管理")
        tab_widget.addTab(image_tab, "影像管理")
        # tab_widget.addTab(user_tab, "用户管理")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
