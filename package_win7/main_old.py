# 导入系统模块，用于处理命令行参数和程序退出
import sys
if sys.version_info < (3,8) or sys.version_info >= (3,11):
    sys.exit("Requires Python 3.8-3.10")
import logging
logging.basicConfig(
        filename='app.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
        )
import os
# 从 PyQt5 模块中导入需要的类
from PyQt5.QtWidgets import (   #从PyQt5.QtWidgets模块中导入需要的组件
    QApplication,  # 应用程序对象
    QWidget,       # 基础窗口控件
    QVBoxLayout,   # 垂直布局
    QHBoxLayout,   # 水平布局
    QPushButton,   # 按钮控件
    QStackedLayout, # 堆叠布局（用于页面切换）
    QFileDialog,   # QFileDialog用于打开文件选择对话框
    QMessageBox,   # QMessageBox用于显示弹出提示或错误信息
    QProgressBar,   # 进度条控件
    QFrame,         #框架控件，包括其它控件
    QLabel,         #标签栏显示进度
)

from PyQt5.QtCore import Qt  # Qt核心模块（包含枚举常量）
from PyQt5.QtGui import QDragEnterEvent, QDropEvent,QLinearGradient, QColor, QPainter  # 拖拽事件相关
import pandas as pd         #导入表格数据处理库
import re                   # re库用于正则表达式操作
import natsort              # 自然排序库
import sort_number
import concat
import split_excel
from generate_all import Generate_all

#***********************主窗口***********************************************
# 主窗口类，继承自 QWidget
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  # 调用父类 QWidget 的构造函数
        self.init_ui()      # 初始化用户界面
        self.setMinimumSize(800, 600)  # 设置窗口最小尺寸（宽度800，高度600）
    # ***********************主窗口***********************************************


    # 初始化用户界面方法
    def init_ui(self):
        # 设置窗口标题
        self.setWindowTitle("智能物料处理系统 v2.0                                              作者:唐健伟")
        # 创建垂直布局作为主布局，并设置边距和间距
        main_layout = QVBoxLayout(self)  # 创建垂直布局，self表示设置给当前窗口
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置布局边距（左，上，右，下）
        main_layout.setSpacing(15)  # 设置控件之间的间距
        # 创建顶部标签切换容器（使用QFrame作为容器）
        tab_bar = QFrame()  # 创建一个框架来包含标签按钮
        tab_bar_layout = QHBoxLayout(tab_bar)  # 使用水平布局管理标签按钮
        tab_bar_layout.setContentsMargins(0, 0, 0, 0)  # 去除布局边距
        tab_bar_layout.setSpacing(0)  # 去除按钮之间的间距
        # 创建标签按钮列表
        self.tab_buttons = []  # 用于存储所有标签按钮
        for text in ["一键生成","分步操作",]:  # 遍历标签名称
            btn = QPushButton(text)  # 创建按钮
            btn.setFixedSize(120, 40)  # 设置按钮固定尺寸（宽度120，高度40）
            btn.setCheckable(True)  # 启用可选中状态（类似单选按钮）
            # btn.setObjectName(f"btn_{text}")
            btn.setObjectName("btn_{}".format(text))
            tab_bar_layout.addWidget(btn)  # 将按钮添加到布局
            self.tab_buttons.append(btn)  # 将按钮添加到列表中
        self.tab_buttons[0].setChecked(True)  # 默认选中第一个标签
        main_layout.addWidget(tab_bar)  # 将标签栏添加到主布局
        # 创建堆叠布局用于管理不同页面
        self.stacked_layout = QStackedLayout()
        # 创建一键生成页面
        self.create_generate_page()
        # 创建分步操作页面
        self.create_step_page()
        main_layout.addLayout(self.stacked_layout)
        # 遍历标签按钮列表，为每个按钮绑定点击事件
        for index, btn in enumerate(self.tab_buttons):
            btn.clicked.connect(lambda _, idx=index: self.switch_tab(idx))
        # 使用CSS样式表美化界面
        self.setStyleSheet(css_content)

# **************************创建一键生成页面********************************************
    def create_generate_page(self):
        page = QWidget()  # 创建一个页面容器
        layout = QVBoxLayout(page)  # 使用垂直布局管理页面内容
        # 创建一键生成按钮
        self.btn_generate_all = QPushButton("一键生成",objectName="btn_generate_all")
        self.btn_generate_all.setFixedHeight(80)  # 设置按钮固定高度
        self.btn_generate_all.clicked.connect(self.generate_all)  # 绑定点击事件
        layout.addWidget(self.btn_generate_all)  # 将按钮添加到布局
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)  # 设置进度条范围（0到100）
        layout.addWidget(QLabel("当前进度："))  # 添加标签
        layout.addWidget(self.progress_bar)  # 添加进度条
        # 将页面添加到堆叠布局
        self.stacked_layout.addWidget(page)


# ************************ 创建分步操作页面**********************************************
    def create_step_page(self):
        page = QWidget()  # 创建一个页面容器
        layout = QVBoxLayout(page)  # 使用垂直布局管理页面内容
        # 定义按钮列表（按钮名称和对应的槽函数）
        buttons = [
            ("位号排序", self.sort_numbers),
            ("料表位号拆分", self.split_numbers),
            ("物料结合", self.combine_materials),
        ]
        # 遍历按钮列表，创建按钮并添加到页面
        for text, func in buttons:
            btn = QPushButton(text)  # 创建按钮
            btn.setFixedHeight(50)  # 设置按钮固定高度
            btn.setAcceptDrops(True)  # 启用拖拽接收
            # 绑定点击事件，调用文件选择方法
            # btn.clicked.connect(lambda _, f=func: self.handle_file_selection(btn, f))
            btn.clicked.connect(lambda _, f=func:f())
            layout.addWidget(btn)  # 将按钮添加到布局
        # 将页面添加到堆叠布局
        self.stacked_layout.addWidget(page)
# ****************************切换标签页************************************************
    def switch_tab(self, index):
        self.stacked_layout.setCurrentIndex(index)  # 设置堆叠布局的当前页面
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)  # 更新按钮选中状态

# ****************************获取按钮对应的槽函数************************************************

    def get_slot_function(self, button_text):
        if button_text == "位号排序":
            return self.sort_numbers
        elif button_text == "料表位号拆分":
            return self.split_numbers
        elif button_text == "物料结合":
            return self.combine_materials
        elif button_text == "执行一键生成":
            return self.generate_all
        return None
 # *****************************位号排序功能***********************************************

    # 定义一个函数sort_numbers，参数file_path默认为None
    def sort_numbers(self, file_path=None):
        # 如果file_path为None，表示还没有文件路径，需要打开对话框选择文件
        file_path, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口，通常是self
            "选择坐标文件",  # 对话框的标题
            "",  # 初始打开的目录，空字符串表示默认目录
            "坐标文件 (*.txt)"  # 文件过滤器，显示*.txt文件
        )
        # 在此处添加实际的位号排序逻辑
        sort_number.process_txt_file(file_path)
        # 例如，读取文件内容，处理数据，然后更新进度条
        QMessageBox.information(self, "提示", "位号排序完成！")
        self.progress_bar.setValue(30)

# *****************************料表位号拆分功能***********************************************
    def split_numbers(self, file_path=None):
        # 如果file_path为None，表示还没有文件路径，需要打开对话框选择文件
        file_path, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口，通常是self
            "选择料表",  # 对话框的标题
            "",  # 初始打开的目录，空字符串表示默认目录
            "料表文件文件 (*.xlsx)"  # 文件过滤器，显示*.xlsx文件
        )
        # 在此处添加实际的料表位号拆分逻辑
        split_excel.process_excel(file_path)
        # 例如，读取文件内容，处理数据，然后更新进度条
        QMessageBox.information(self, "提示", "料表位号拆分完成！")
        self.progress_bar.setValue(60)
# *****************************物料结合功能***********************************************

    def combine_materials(self, file_path=None):
        if file_path is None:
            # 通过点击按钮选择文件
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择拆分料表",  # 标题
                "",  # 初始目录
                "文本文件 (*.xlsx);"  # 文件过滤器
            )
            if not file_path:
                return  # 如果用户取消选择，返回
        # 在此处添加实际的物料结合逻辑
        concat.process_concat(file_path)
        # 例如，读取文件内容，处理数据，然后更新进度条
        QMessageBox.information(self, "提示", "物料结合完成！")
        self.progress_bar.setValue(90)

# *****************************一键生成功能***********************************************

    def generate_all(self, txt_path=None,excel_path=None):
        generate = Generate_all()
        print(txt_path,excel_path)
    # *****************************加载txt***********************************************
        # 如果file_path为None，表示还没有文件路径，需要打开对话框选择文件
        txt_path, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口，通常是self
            "选择坐标文件",  # 对话框的标题
            "",  # 初始打开的目录，空字符串表示默认目录
            "坐标文件 (*.txt)"  # 文件过滤器，显示*.txt文件
        )
        # 在此处添加实际的位号排序逻辑
        generate.process_txt_file(txt_path)
        # 例如，读取文件内容，处理数据，然后更新进度条
        QMessageBox.information(self, "提示", "位号排序完成！")
        self.progress_bar.setValue(30)
        # 如果file_path为None，表示还没有文件路径，需要打开对话框选择文件

    # *****************************加载excel***********************************************
        excel_path, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口，通常是self
            "选择料表",  # 对话框的标题
            "",  # 初始打开的目录，空字符串表示默认目录
            "料表文件文件 (*.xlsx)"  # 文件过滤器，显示*.xlsx文件
        )
        # 在此处添加实际的料表位号拆分逻辑
        generate.process_excel(excel_path)
        # 例如，读取文件内容，处理数据，然后更新进度条
        QMessageBox.information(self, "提示", "料表位号拆分完成！")
        self.progress_bar.setValue(60)
    # *****************************料表结合***********************************************
        generate.process_cancat()
        QMessageBox.information(self, "提示", "物料结合完成！")
        self.progress_bar.setValue(90)
    # *****************************料表结合***********************************************
        QMessageBox.information(self, "完成", "所有操作执行完毕！")  # 显示消息框
        self.progress_bar.setValue(100)  # 更新进度条

# *****************************加载文件方法***********************************************
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# *****************************程序入口***********************************************

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序对象
    with open('../style.css', 'r', encoding='utf-8') as file:
        css_content = file.read()
    # css_path = resource_path("style.css")
    # with open(css_path, 'r') as f:
    #     css_content = f.read()
    window = MainWindow()  # 创建主窗口对象
    window.show()  # 显示主窗口
    sys.exit(app.exec())  # 进入应用程序主循环

'''
详细解释


导入模块

sys：用于处理命令行参数和程序退出。

PyQt5.QtWidgets：导入GUI控件，如窗口、按钮、布局等。

PyQt5.QtCore：导入核心功能，如枚举常量。

PyQt5.QtGui：导入图形界面相关功能，如拖拽事件。



MainWindow类

继承自QWidget，用于创建主窗口。

__init__方法：初始化窗口，调用init_ui方法，设置最小尺寸。

init_ui方法：初始化用户界面，设置标题，创建布局，添加控件，设置样式。



布局管理

main_layout：垂直布局，管理整个窗口的控件。

tab_bar：使用QFrame和水平布局管理标签按钮。

stacked_layout：堆叠布局，用于管理不同页面的切换。



标签切换栏

创建三个标签按钮：“分步操作”、“一键生成”、“进度监控”。

每个按钮设置为可选中状态，点击时切换页面。



页面创建

create_step_page：创建分步操作页面，包含四个按钮，支持文件拖拽和选择。

create_generate_page：创建一键生成页面，包含一个大按钮。

create_progress_page：创建进度监控页面，包含进度条和标签。



信号与槽

标签按钮点击事件连接到switch_tab方法，切换页面。

文件选择和拖拽事件连接到相应的方法，处理文件操作。



样式表

使用CSS样式美化界面，设置背景图片、字体等。



业务功能

模拟位号排序、料表拆分、物料结合和一键生成功能，更新进度条并显示消息框。



程序入口

创建QApplication对象，实例化MainWindow，显示窗口，进入主循环。
通过以上步骤，这段代码创建了一个功能完善的GUI应用程序，包含多个页面和交互功能，适合初学者学习PyQt5的基本用法。

'''