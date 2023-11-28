# 导入PyQt5模块
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QGridLayout
from PyQt5.QtCore import Qt
import re

# 定义文法规则
rules = {
    "E": ["TG"],
    "G": ["+TG", "-TG", ""],
    "T": ["FS"],
    "S": ["*FS", "/FS", ""],
    "F": ["(E)", "i"]
}

# 定义终结符和非终结符以及正则表达式
terminals = ["+", "-", "*", "/", "(", ")", "i", "#"]
nonterminals = ["E", "G", "T", "S", "F"]
regex = r'[^*+-/()i#]'

# 定义分析表，字典值为空表示ε
table = {
    ("E", "+"): None,
    ("E", "-"): None,
    ("E", "*"): None,
    ("E", "/"): None,
    ("E", "("): "TG",
    ("E", ")"): None,
    ("E", "i"): "TG",
    ("E", "#"): None,
    ("G", "+"): "+TG",
    ("G", "-"): "-TG",
    ("G", "*"): None,
    ("G", "/"): None,
    ("G", "("): None,
    ("G", ")"): "",
    ("G", "i"): None,
    ("G", "#"): "",
    ("T", "+"): None,
    ("T", "-"): None,
    ("T", "*"): None,
    ("T", "/"): None,
    ("T", "("): "FS",
    ("T", ")"): None,
    ("T", "i"): "FS",
    ("T", "#"): None,
    ("S", "+"): "",
    ("S", "-"): "",
    ("S", "*"): "*FS",
    ("S", "/"): "/FS",
    ("S", "("): None,
    ("S", ")"): "",
    ("S", "i"): None,
    ("S", "#"): "",
    ("F", "+"): None,
    ("F", "-"): None,
    ("F", "*"): None,
    ("F", "/"): None,
    ("F", "("): "(E)",
    ("F", ")"): None,
    ("F", "i"): "i",
    ("F", "#"): None,
}

# 定义分析函数


def analyze(input_string):
    # 定义分析栈
    stack = ["#", "E"]
    # 定义输出结果
    output = ""
    # 输出过程如下
    output += "输出过程如下：\n"
    # 添加格式化输出
    output += "{:<10}{:<20}{:<20}{:<20}\n".format(
        "步骤", "分析栈", "剩余输入串", "所用产生式")
    step = 1  # 记录步骤
    while True:
        # 获取栈顶符号和输入串首符号
        top = stack[-1]
        first = input_string[0]
        # 如果栈顶符号和输入串首符号都是#
        if top == "#" and first == "#":
            # 输出分析成功
            production = "分析成功"
            output += "{:<10}{:<20}{:<20}{:<20}\n".format(
                step, ''.join(stack), input_string, production)  # 添加格式化输出
            break
        # 如果栈顶符号是终结符或者#
        elif top in terminals or top == "#":
            # 如果栈顶符号和输入串首符号相同
            if top == first:
                # 输出匹配终结符
                production = f"“{top}”匹配"
                output += "{:<10}{:<20}{:<20}{:<20}\n".format(
                    step, ''.join(stack), input_string, production)  # 添加格式化输出
                # 弹出栈顶符号
                stack.pop()
                # 去掉输入串首符号
                input_string = input_string[1:]
                # 步骤加一
                step += 1
            # 否则
            else:
                # 输出分析出错
                production = "分析出错"
                output += "{:<10}{:<20}{:<20}{:<20}\n".format(
                    step, ''.join(stack), input_string, production)  # 添加格式化输出
                break
        # 如果栈顶符号是非终结符
        elif top in nonterminals:
            # 如果分析表中有对应的产生式
            if table[(top, first)] is not None:
                # 获取产生式右部
                right = table[(top, first)]
                # 输出所用产生式
                production = f"{top}->{right}"
                output += "{:<10}{:<20}{:<20}{:<20}\n".format(
                    step, ''.join(stack), input_string, production)  # 添加格式化输出
                # 弹出栈顶符号
                stack.pop()
                # 如果产生式右部不是空
                if right != "":
                    # 将产生式右部逆序压入栈中
                    for symbol in right[::-1]:
                        stack.append(symbol)
                # 步骤加一
                step += 1
            # 否则
            else:
                # 输出分析出错
                production = "分析出错"
                output += "{:<10}{:<20}{:<20}{:<20}\n".format(
                    step, ''.join(stack), input_string, production)  # 添加格式化输出
                break
        # 否则
        else:
            # 输出分析出错
            production = "分析出错"
            output += "{:<10}{:<20}{:<20}{:<20}\n".format(
                step, ''.join(stack), input_string, production)  # 添加格式化输出
            break
    # 返回输出结果
    return output

# 定义主窗口类


class MainWindow(QWidget):
    # 初始化方法
    def __init__(self):
        # 调用父类初始化方法
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("LL（1）分析程序，编制人：孙成，2150810317，21508013")
        # 设置窗口大小
        self.resize(1200, 900)
        # 创建标签控件
        self.label1 = QLabel("输入一以#结束的符号串(包括+—*/()i#):", self)
        self.label2 = QLabel("输出结果:", self)
        self.label3 = QLabel("分析结果:", self)
        self.label3Out = QLineEdit('', self)
        self.label3Out.setReadOnly(True)
        self.label4 = QLabel(
            '''文法如下：
            (1)E->TG
            (2)G->+TG|—TG
            (3)G->ε
            (4)T->FS
            (5)S->*FS|/FS
            (6)S->ε
            (7)F->(E)
            (8)F->i
            ''')
        # 创建文本框控件
        self.input = QLineEdit(self)
        # 创建按钮控件
        self.button = QPushButton("分析", self)
        # 创建文本编辑控件
        self.output = QTextEdit(self)
        # 设置文本编辑控件为只读
        self.output.setReadOnly(True)
        # 创建网格布局
        self.layout = QGridLayout(self)
        # 添加控件到布局中
        self.layout.addWidget(self.label1, 0, 0)
        self.layout.addWidget(self.input, 0, 1)
        self.layout.addWidget(self.button, 0, 2)
        self.layout.addWidget(self.label2, 1, 0)
        self.layout.addWidget(self.output, 2, 0, 1, 3)
        self.layout.addWidget(self.label3, 3, 0, 1, 3)
        self.layout.addWidget(self.label3Out, 3, 1, 1, 1)
        self.layout.addWidget(self.label4, 4, 0, 1, 3)
        # 设置布局
        self.setLayout(self.layout)
        # 绑定按钮点击事件
        self.button.clicked.connect(self.on_click)

    # 定义按钮点击事件处理函数
    def on_click(self):
        # 获取输入串
        input_string = self.input.text()
        # 检查输入串是否合法
        if re.findall(regex, input_string):
            self.output.setText("输入串只能包含+-*/()i#")
        elif input_string.endswith("#"):
            # 调用分析函数
            output = analyze(input_string)
            # 显示输出结果
            self.output.setText(output)
        else:
            # 显示错误信息
            self.output.setText("输入串必须以#结束！")

        try:
            if re.findall("\u51fa\u9519", output):
                self.label3Out.setText("分析出错")
            else:
                self.label3Out.setText("分析成功")
        except:
            pass


# 创建应用对象
app = QApplication([])
# 创建主窗口对象
window = MainWindow()
# 显示主窗口
window.show()
# 运行应用
app.exec_()
