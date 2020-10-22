import csv
import logging
import os
import pickle
import sys

import pymysql
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QPushButton
import numpy as np

Column = 6
Row = 20


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.table = QTableWidget(self)
        self.table.move(20, 20)
        self.table.setColumnCount(Column)
        self.table.setRowCount(Row)
        self.table.setFixedHeight(300)
        self.table.setFixedWidth(600)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格的选取方式是行选取
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置选取方式为单个选取
        self.table.setHorizontalHeaderLabels(["螺丝编号", "电路板型号", "标准力矩", "标准转角", "坐标x", "坐标y"])  # 设置行表头
        self.table.verticalHeader().setVisible(False)  # 隐藏列表头
        path = "table.csv"
        create = not QFile.exists(path)
        if create:

            self.table_create()
        else:
            with open(path, 'r') as f:
                csv_read = csv.reader(f)
                row = 0
                for line in csv_read:
                    # print(line)

                    for col in range(line.__len__()):
                        temp = QTableWidgetItem(str(line[col]))
                        if col == 1 or col == 4 or col == 5:
                            temp.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.table.setItem(row, col, temp)

                        # print(self.table.item(i,col).text())
                    row = row + 1

        # self.table.itemChanged.connect(self.table_update)

        self.save_button = QPushButton(self)
        self.save_button.move(250, 350)
        self.save_button.setFixedWidth(100)
        self.save_button.setFixedHeight(32)
        self.save_button.clicked.connect(self.table_save)
        self.save_button.setText("save")

        self.setGeometry(200, 200, 650, 400)
        self.show()

        # 以下可以加入保存数据到数据的操作
        '''
        eg. update {table} set name = "new_name" where id = "id"
        '''

        # delete
        # def table_delete(self):
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))

        row = row_select[0].row()
        self.table.removeRow(row)
        # 以下可以加入保存数据到数据的操作
        '''
        eg. delete from {table} where id = "id"
        '''

    def table_create(self):
        # row = self.table.rowCount()
        # self.table.insertRow(row)
        screw_id = ["1"] * Row

        # item_name = QTableWidgetItem("door")  # 我们要求它可以修改，所以使用默认的状态即可
        #
        # item_pos = QTableWidgetItem("1")

        for row in range(1, Row + 1):
            screw_id[row - 1] = QTableWidgetItem(str(row))
            screw_id[row - 1].setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            pcbType = QTableWidgetItem("1234567")  # 我们要求它可以修改，所以使用默认的状态即可
            torque = QTableWidgetItem("1")
            angle = QTableWidgetItem("100")
            x = QTableWidgetItem("0")
            y = QTableWidgetItem("0")
            self.table.setItem(row - 1, 0, screw_id[row - 1])
            self.table.setItem(row - 1, 1, pcbType)
            self.table.setItem(row - 1, 2, torque)
            self.table.setItem(row - 1, 3, angle)
            self.table.setItem(row - 1, 4, x)
            self.table.setItem(row - 1, 5, y)

    def table_save(self):
        QSqlDatabase.database().commit()
        path = "table.csv"

        with open(path, 'w', newline='') as f:
            csv_write = csv.writer(f)

            for row in range(0, Row):
                data = []
                for col in range(0, Column):
                    data.append(self.table.item(row, col).text())

                # data.append('\n')
                print(data)
                csv_write.writerow(data)
            print(data)
            # data = data_row.append(data_row)
            # csv_write.writerow(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TableWindow()
    sys.exit(app.exec_())
