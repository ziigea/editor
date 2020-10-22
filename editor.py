import csv
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QLineEdit, QDialog, QTableWidget, \
    QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QPoint, pyqtSignal, QFile
from PyQt5.QtGui import QDrag, QPalette, QBrush, QPixmap
from PyQt5 import QtGui, QtCore, QtWidgets, QtSql
import time

num = 30
Column = 5
coordinate_x = [0] * num
coordinate_y = [0] * num
table = []


class MyDialog(QDialog):
    # 自定义信号
    mySignal = pyqtSignal(str)
    data = []

    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.table = QTableWidget(self)
        self.table.move(10, 10)
        self.table.setColumnCount(3)
        self.table.setRowCount(1)
        self.table.setFixedHeight(56)
        self.table.setFixedWidth(318)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格的选取方式是行选取
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置选取方式为单个选取
        self.table.setHorizontalHeaderLabels(["电路板型号", "标准力矩", "标准转角"])  # 设置行表头

        self.save_button = QPushButton("保存", self)
        self.save_button.move(130, 70)
        self.save_button.setFixedWidth(100)
        self.save_button.setFixedHeight(32)

        self.save_button.clicked.connect(self.sendEditContent)
        self.setWindowTitle('螺丝参数详情')
        self.setGeometry(440, 440, 340, 110)

        self.show()

    def sendEditContent(self):
        # data = []
        # for col in range(5):
        # data.append(self.table.item(0, col).text())

        data = ','.join([self.table.item(0, 0).text(), self.table.item(0, 1).text(), self.table.item(0, 2).text()])

        # print(data)
        self.mySignal.emit(str(data))  # 发射信号


class DraggableButton(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.iniDragCor = [0, 0]
        self.num = int(title)
        # print(self.num)

    def mousePressEvent(self, e):
        print("click", e.pos())
        self.iniDragCor[0] = e.x()
        self.iniDragCor[1] = e.y()

    def mouseMoveEvent(self, e):
        x = e.x() - self.iniDragCor[0]
        y = e.y() - self.iniDragCor[1]

        cor = QPoint(x, y)
        self.move(self.mapToParent(cor))  # 需要maptoparent一下才可以的,否则只是相对位置。

        # print('drag button event,', time.time(), e.pos(), e.x(), e.y())

        # print()
        coordinate_x[self.num - 1] = self.geometry().x()
        coordinate_y[self.num - 1] = self.geometry().y()

    def mouseDoubleClickEvent(self, e):
        print("Doubleclick", e.pos())
        self.mydialog = MyDialog()
        self.mydialog.mySignal.connect(self.getDialogSignal)
        self.mydialog.exec_()

    def getDialogSignal(self, connect):
        # screw = list(str(self.num))
        screw = connect.split(',')
        # screw = screw + data
        print("screw",screw)
        print("table",table)
        for i in range(num):
            if table[i][0] == str(self.num):
                print(table[i][0])
                table[i][1] = screw[0]
                table[i][2] = screw[1]
                table[i][3] = screw[2]
                print("yyyy",table)
                break


class EditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        button = {}

        for i in range(num, -1, -1):
            button[i] = DraggableButton(str(i + 1), self)
            # self.button1 = DraggableButton("1", self)
            # self.button1.move(50, 20)
            button[i].setGeometry(50, 50, 20, 20)
            button[i].setStyleSheet("background-color: rgb(0, 0, 255);"
                                    "border-color: rgb(255, 255, 163);"
                                    "font: 75 12pt \"Arial Narrow\";"
                                    "color: rgb(255, 255, 0);")

        # # 创建一个表格部件
        # self.table_widget = QtWidgets.QTableView()
        # # 将上述两个部件添加到网格布局中
        #
        # self.table_widget.setGeometry(10, 10, 20, 20)

        self.mark_button = QPushButton("记录位置", self)
        self.mark_button.move(50, 10)
        self.mark_button.resize(80, 30)
        self.mark_button.clicked.connect(self.saveTable)

        palette = QPalette()
        picture = QPixmap("2.png")
        palette.setBrush(QPalette.Background, QBrush(picture))
        self.setPalette(palette)
        self.setWindowTitle("Click or Move")
        self.setGeometry(100, 100, picture.width(), picture.height())

        self.show()

    def mouseMoveEvent(self, e):
        print('main', e.x(), e.y())

    def saveTable(self):
        for i in range(num):
            if coordinate_x[i] and coordinate_y[i]:
                print("第", i + 1, "个螺丝坐标", coordinate_x[i], coordinate_y[i])
                table[i][4] = str(coordinate_x[i])
                table[i][5] = str(coordinate_y[i])

        print(table)
        path = "table.csv"

        with open(path, 'w', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerows(table)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    path = "table.csv"
    create = not QFile.exists(path)
    if create:
        for i in range(30):
                table.append([str(i + 1), '0', '0', '0', '0', '0'])
    else:
        with open(path, 'r') as f:
            csv_read = csv.reader(f)
            row = 0
            for line in csv_read:
                table.append(line)

    ex = EditorWindow()
    ex.show()
    app.exec_()
