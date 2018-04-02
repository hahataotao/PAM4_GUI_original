import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from BER_setting import Ui_setting
class dockdemo(QMainWindow):
    def __init__(self, parent=None):
        super(dockdemo, self).__init__(parent)

        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("save")
        file.addAction("quit")

        self.items = QDockWidget("Dockable", self)
        self.listWidget = QListWidget()
        self.listWidget.addItem("item1")
        self.listWidget.addItem("item2")
        self.listWidget.addItem("item3")
        self.b1=QPushButton('test')

        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)
        self.setLayout(layout)
        self.setWindowTitle("Dock demo")
class My(QDialog):
    def __init__(self):
        super(My,self).__init__()
        self.ui=Ui_setting()
        self.ui.setupUi(self)

def main():
    app = QApplication(sys.argv)
    ex =My()
    ex.show()
    ex.exec_()


if __name__ == '__main__':
    main()