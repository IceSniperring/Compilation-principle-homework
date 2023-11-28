# 导入pyqt5模块
from PyQt5 import QtCore, QtGui, QtWidgets
import re

# 定义递归下降分析器类
class RecursiveDescentParser:
    def __init__(self):
        self.grammar = {
            'E': ['TG'],
            'G': ['+TG', '-TG', ''],
            'T': ['FS'],
            'S': ['*FS', '/FS', ''],
            'F': ['(E)', 'i']
        }
        self.input_string = ''
        self.index = 0
        self.regex = r'[^*+-/()i#]'

    def parse(self, input_string):
        self.input_string = input_string
        self.index = 0
        if self.E() and self.match('#'):
            return f'{input_string}为合法符号串'
        elif re.findall(self.regex, input_string):
            return f'{input_string}为非法符号串,原因：存在非法符号'
        else:
            return f'{input_string}为非法符号串,原因：符号多余或者未以#结尾'

    def match(self, token):
        if self.index < len(self.input_string) and self.input_string[self.index] == token:
            self.index += 1
            return True
        else:
            return False

    def E(self):
        return self.production('E')

    def G(self):
        return self.production('G')

    def T(self):
        return self.production('T')

    def S(self):
        return self.production('S')

    def F(self):
        return self.production('F')

    def production(self, nonterminal):
        for production in self.grammar[nonterminal]:
            saved_index = self.index
            if all(self.match(token) if token not in self.grammar else getattr(self, token)() for token in production):
                return True
            self.index = saved_index
        return False

# 定义pyqt5界面类
class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1250, 200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tip = QtWidgets.QLabel(self.centralwidget)
        self.tip.setGeometry(QtCore.QRect(50, 0, 1000, 50))
        self.tip.setObjectName("tip")
        self.input_line = QtWidgets.QLineEdit(self.centralwidget)
        self.input_line.setGeometry(QtCore.QRect(50, 50, 1000, 50))
        self.input_line.setObjectName("input_line")
        self.analyze_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_button.setGeometry(QtCore.QRect(1100, 50, 100, 50))
        self.analyze_button.setObjectName("analyze_button")
        self.output_label = QtWidgets.QLabel(self.centralwidget)
        self.output_label.setGeometry(QtCore.QRect(50, 100, 491, 31))
        self.output_label.setObjectName("output_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.analyze_button.clicked.connect(self.analyze)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.tip.setText(_translate("MainWindow", "输入一以#结束的符号串(包括+—*/()i#)"))
        MainWindow.setWindowTitle(_translate("MainWindow", "递归下降分析程序，编制人：孙成，2150810317，21508013"))
        self.analyze_button.setText(_translate("MainWindow", "分析"))
        self.output_label.setText(_translate("MainWindow", ""))

    def analyze(self):
        input_string = self.input_line.text()
        parser = RecursiveDescentParser()
        result = parser.parse(input_string)
        self.output_label.setText(result)


# 测试pyqt5界面
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

