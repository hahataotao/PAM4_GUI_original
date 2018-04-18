import sys
# sys.path.append('C:/PAM4_GUI/Controls')
# sys.path.append('C:/PAM4_GUI/Model')
# sys.path.append('C:/PAM4_GUI/Views')
from PyQt4 import QtGui
from Model.Model import Model
from Controls.Ctrls import MainController
from Views.main_view import Window,WaitBoxWindow
import os
class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        initFileDirectory = os.getcwd()+"/"
        initFileName = "BER_InitFile_V100_SY.json"
        self.main_ctrl = MainController(initFileDirectory,initFileName,self.model)
        #show the windows
        self.main_view = Window(self.model, self.main_ctrl)
        #self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())