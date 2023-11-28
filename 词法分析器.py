# 导入pyqt5模块
from PyQt5 import QtCore, QtGui, QtWidgets
import re

# 定义种别码
token_dict = {
    'main': 1,
    'printf': 1,
    'if': 1,
    'int': 1,
    'for': 1,
    'while': 1,
    'do': 1,
    'return': 1,
    'break': 1,
    'continue': 1,
    '+': 4,
    '-': 4,
    '*': 4,
    '/': 4,
    '=': 4,
    '>': 4,
    '<': 4,
    '>=': 4,
    '<=': 4,
    '!=': 4,
    ',': 5,
    ';': 5,
    '{': 5,
    '}': 5,
    '(': 5,
    ')': 5
}

# 定义词素的正则表达式
regex_patterns = [
    (r'[a-zA-Z_][a-zA-Z_0-9]*', 2),
    (r'\d+', 3),
    (r'\S', 0)
]


def lexical_analyzer(code):
    tokens = []
    while code:
        code = code.lstrip()
        for pattern, type_code in regex_patterns:
            match = re.match(pattern, code)
            if match:
                lexeme = match.group()
                if lexeme in token_dict:
                    type_code = token_dict[lexeme]
                tokens.append((type_code, lexeme))
                code = code[len(lexeme):]
                break
    return tokens


# 定义pyqt5界面类
class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1350, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.output_text = QtWidgets.QTextEdit(self.centralwidget)
        self.output_text.setGeometry(QtCore.QRect(700, 50,600, 300))
        self.output_text.setObjectName("output_text")
        self.output_text.setReadOnly(True)
        self.analyze_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_button.setGeometry(QtCore.QRect(625, 350, 93, 28))
        self.analyze_button.setObjectName("analyze_button")
        # 添加文件选择按钮
        self.file_button = QtWidgets.QPushButton(self.centralwidget)
        self.file_button.setGeometry(QtCore.QRect(50, 50, 120, 50))
        self.file_button.setObjectName("file_button")
        # 添加文件显示区域
        self.file_text = QtWidgets.QTextEdit(self.centralwidget)
        self.file_text.setGeometry(QtCore.QRect(200, 50, 400, 300))
        self.file_text.setObjectName("file_text")
        self.file_text.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.analyze_button.clicked.connect(self.analyze)
        self.file_button.clicked.connect(self.select_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "词法分析器"))
        self.analyze_button.setText(_translate("MainWindow", "分析"))
        self.file_button.setText(_translate("MainWindow", "选择文件"))
        self.file_text.setText(_translate("MainWindow", "请选择文件"))
        self.output_text.setText(_translate("MainWindow", "词法分析结果"))

    def analyze(self):
        # 从文件中读取代码
        try:
            with open(self.file_name, 'r') as f:
                code = f.read()
        except:
            code = ""
        tokens = lexical_analyzer(code)
        output = ""
        for token in tokens:
            output += str(token) + "\n"
        self.output_text.setText(output)

    def select_file(self):
        # 弹出文件选择对话框
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "", "c语言文件 (*.c)")
        # 在文件显示区域中显示文件名和内容
        try:
            with open(self.file_name, 'r') as f:
                    file_content = f.read()
        except:
            file_content = "错误，文件中可能含有中文"
        self.file_text.setText("文件名: " + self.file_name + "\n\n" + "文件内容: \n" + file_content)



# 测试pyqt5界面
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
