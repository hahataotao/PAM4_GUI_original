from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPalette,QBrush
import os
import sys
from decimal import Decimal
from waitbox import Ui_Form
from BER_setting import Ui_setting


class hiddenBERDialog(QtGui.QDialog):
    def __init__(self):
        super(hiddenBERDialog, self).__init__()
        self.ui = Ui_setting()
        self.ui.setupUi(self)

class WaitBoxWindow(QWidget,Ui_Form):
    def __init__(self,parent=None):
        #super(WaitBoxWindow,self).__init_()
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        #Adjust the position of the waiting box
        self.move(QtGui.QApplication.desktop().rect().center() - self.rect().center())

# creation of the class, one specifies that one derives the class QPushButton between parentheses
class PushButtonRight(QtGui.QPushButton):
    # creation of the emitter signal (emet nothing for the moment)
    rightClick = QtCore.pyqtSignal()

    # creation of our function __init__ with an arg string for the name of the future button
    def __init__(self, string):
        # on integrate the QPushButton class with our PushRightButton class
        QtGui.QPushButton.__init__(self, string)
        #super(QtGui.QPushButton,self).__init__(self,string)

    # modification of the mousePressEvent function
    def mousePressEvent(self, event):
        # on integrate QPushButton.mousePressEvent function (self, event) to our function PushRightButton.mousePressEvent (self, event)
        QtGui.QPushButton.mousePressEvent(self, event)

        # condition of the right click
        if event.button() == QtCore.Qt.RightButton:
            # emittion of rightClick signal
            self.rightClick.emit()
            print ('3 click of mouse')
#handle display GUI view
class Window(QWidget):
    # properties to read/write widget value
    @property
    def runningCh0Err(self):
        return self.totalNoErrCh0.text()
    @property
    def runningCh0Ber(self):
        return self.berCh0.text()

    @property
    def runningCh1Err(self):
        return self.totalNoErrCh1.text()
    @property
    def runningCh1Ber(self):
        return self.berCh1.text()

    @property
    def runningCh2Err(self):
        return self.totalNoErrCh2.text()

    @property
    def runningCh2Ber(self):
        return self.berCh2.text()
    @property
    def runningCh3Err(self):
        return self.totalNoErrCh3.text()

    @property
    def runningCh3Ber(self):
        return self.berCh3.text()
    @property
    def getAttrSliderValue(self):
        return self.slsetAttr.value()
    @property
    def runningTransmittedBit(self):
        return self.txtTransmitterBits.text()
    @runningTransmittedBit.setter
    def runningTransmittedBit(self,value):
        return self.txtTransmitterBits.setText("{:.2E}".format(Decimal(value)))
    @property
    def runningTimeElapsed(self):
        return self.txtElapsedTime.text()
    @runningTimeElapsed.setter
    def runningTimeElapsed(self,value):
        return self.txtElapsedTime.setText(str(value))
    @getAttrSliderValue.setter
    def getAttrSliderValue(self,value):
        self.lblAttrValue.setText('Set Attr. ' + str(float(value) / 2) + ' dB')
    @runningCh0Ber.setter
    def runningCh0Ber(self,value):
        return self.berCh0.setText("{:.2E}".format(Decimal(value)))
    @runningCh0Err.setter
    def runningCh0Err(self, value):
        self.totalNoErrCh0.setText(str(value))

    @runningCh1Ber.setter
    def runningCh1Ber(self, value):
        return self.berCh1.setText("{:.2E}".format(Decimal(value)))

    @runningCh1Err.setter
    def runningCh1Err(self, value):
        self.totalNoErrCh1.setText(str(value))

    @runningCh2Ber.setter
    def runningCh2Ber(self, value):
        return self.berCh2.setText("{:.2E}".format(Decimal(value)))

    @runningCh2Err.setter
    def runningCh2Err(self, value):
        self.totalNoErrCh2.setText(str(value))

    @runningCh3Ber.setter
    def runningCh3Ber(self, value):
        return self.berCh3.setText("{:.2E}".format(Decimal(value)))

    @runningCh3Err.setter
    def runningCh3Err(self, value):
        self.totalNoErrCh3.setText(str(value))

    def __init__(self,model=None,main_ctrl=None):
        super(Window, self).__init__()
        self.main_ctrl=main_ctrl
        self.model=model
        self.setupMainWindow()
        self.setupAllSignalsSlot()
        self.exit = QtGui.QAction(self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.triggered.connect(self.closeEvent)
        #self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        # register func with model for future model update announcements
        self.model.subscribe_update_func(self.update_ui_from_model)

    def setupTab1GUI(self):
        self.tab1 = QtGui.QTableWidget(self)
        self.tabWidget.addTab(self.tab1, "EyeCapture 100G")

        self.vecticalLayoutWidgetInsideTab1 = QtGui.QWidget(self.tab1)
        self.vecticalLayoutWidgetInsideTab1.setGeometry(20, 10, 411, 511)
        self.gridLayoutWidget = QtGui.QWidget(self.vecticalLayoutWidgetInsideTab1)
        self.gridLayoutWidget.setGeometry(0, 0, 500, 900)
        self.verticalLayoutInsideTab1 = QtGui.QVBoxLayout(self.vecticalLayoutWidgetInsideTab1)
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)

        self.graphicsView_1 = QtGui.QLabel(self.gridLayoutWidget)
        self.graphicsView_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.graphicsView_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.graphicsView_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.graphicsView_1.setAutoFillBackground(True)
        self.graphicsView_2.setAutoFillBackground(True)
        self.graphicsView_3.setAutoFillBackground(True)
        self.graphicsView_4.setAutoFillBackground(True)

        self.graphicsView_1.setGeometry(5, 5, 100, 300)

        self.graphicsView_2.setGeometry(5, 5, 100, 300)
        self.graphicsView_3.setGeometry(5, 5, 100, 300)
        self.graphicsView_4.setGeometry(5, 5, 100, 300)

        self.graphicsView_1.setScaledContents(True)
        self.graphicsView_2.setScaledContents(True)
        self.graphicsView_3.setScaledContents(True)
        self.graphicsView_4.setScaledContents(True)

        self.gridLayout.addWidget(self.graphicsView_1, 1, 0, 3, 1)
        self.gridLayout.addWidget(self.graphicsView_2, 1, 1, 3, 1)
        self.gridLayout.addWidget(self.graphicsView_3, 5, 0, 3, 1)
        self.gridLayout.addWidget(self.graphicsView_4, 5, 1, 3, 1)

        self.label_1 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.lblpartTestForEyeCapture = QtGui.QLabel(self.gridLayoutWidget)
        self.lblImageType = QtGui.QLabel(self.gridLayoutWidget)
        self.txtpartTestForEyeCapture = QtGui.QLineEdit(self.gridLayoutWidget)
        self.cbImagesType = QtGui.QComboBox(self.gridLayoutWidget)
        ImageType = ["CWDM_5e5", "LR4_5e5", "CLR4_0hit"]
        self.cbImagesType.addItems(ImageType)

        self.label_1.setFrameShape(QtGui.QFrame.Box)
        self.label_2.setFrameShape(QtGui.QFrame.Box)
        self.label_3.setFrameShape(QtGui.QFrame.Box)
        self.label_4.setFrameShape(QtGui.QFrame.Box)

        self.label_1.setText("Ch0 1270nm")
        # self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.label_2.setText("Ch1 1290nm")
        # self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1, QtCore.Qt.AlignCenter)
        self.label_3.setText("Ch2 1310nm")
        # self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.label_4.setText("Ch3 1330nm")
        # self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1, QtCore.Qt.AlignCenter)
        self.lblpartTestForEyeCapture.setText("XCVR Test Part Number")
        self.lblImageType.setText("Type of set Images to load")
        self.gridLayout.addWidget(self.lblpartTestForEyeCapture, 8, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.gridLayout.addWidget(self.lblImageType, 8, 1, 1, 1, QtCore.Qt.AlignLeft)

        self.gridLayout.addWidget(self.txtpartTestForEyeCapture, 9, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.gridLayout.addWidget(self.cbImagesType, 9, 1, 1, 1, QtCore.Qt.AlignLeft)

        self.verticalLayoutInsideTab1.addWidget(self.gridLayoutWidget)

        self.horizontalLayoutWidget = QtGui.QWidget(self.vecticalLayoutWidgetInsideTab1)
        self.horizontalLayoutWidget.setGeometry(0, 240, 401, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.labelEyeFolderName = QtGui.QLabel(self.horizontalLayoutWidget)
        self.txtEyeFolderName = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.labelEyeFolderName.setText("Test Folder name==>")
        self.horizontalLayout.addWidget(self.labelEyeFolderName)
        self.horizontalLayout.addWidget(self.txtEyeFolderName)

        self.btneyeTest = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnloadPics = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnloadPics.setEnabled(False)
        self.btneyeTest.setText("Capture Eye")
        self.btnloadPics.setText("LoadImage")
        self.horizontalLayout.addWidget(self.btnloadPics)
        self.horizontalLayout.addWidget(self.btneyeTest)

        self.verticalLayoutInsideTab1.addWidget(self.horizontalLayoutWidget)
        self.tab1.setLayout(self.verticalLayoutInsideTab1)
    def setupTab2GUI(self):
        self.tab2 = QtGui.QTableWidget(self)
        self.tabWidget.addTab(self.tab2, "ModuleControl_QSFP28")
        self.gridLayoutWidgetInsideTab2 = QtGui.QWidget(self.tab2)
        self.gridLayoutWidgetInsideTab2.setGeometry(20, 10, 300, 300)
        self.gridLayoutInsideTab2 = QtGui.QGridLayout(self.gridLayoutWidgetInsideTab2)

        self.idcImodTableWidget = QtGui.QTableWidget(self.gridLayoutWidgetInsideTab2)
        self.idcImodTableWidget.setWindowTitle("Module Idc Imod ")
        self.idcImodTableWidget.setSortingEnabled(False)
        item23 = self.idcImodTableWidget.verticalHeaderItem(0)

        self.idcImodTableWidget.setGeometry(10, 10, 200, 200)
        self.idcImodTableWidget.setToolTip("Module set for Idc & Imod ")
        self.idcImodTableWidget.resize(200, 200)
        self.idcImodTableWidget.setColumnCount(2)
        self.idcImodTableWidget.setRowCount(4)
        self.idcImodTableWidget.setAutoFillBackground(True)

        # set horizontal format
        for i in range(2):
            self.font = QtGui.QFont()
            self.font.setPointSize(9)
            self.font.setBold(True)
            self.font.setWeight(75)
            self.item = QtGui.QTableWidgetItem()
            self.item.setFont(self.font)
            # problem cannot change header background color, research no solution , why???
            self.item.setBackgroundColor(QtGui.QColor(255, 255, 0))
            self.idcImodTableWidget.setHorizontalHeaderItem(i, self.item)

        # set vectical header format
        for i in range(4):
            self.font = QtGui.QFont()
            self.font.setPointSize(9)
            self.font.setBold(True)
            self.font.setWeight(75)
            self.item = QtGui.QTableWidgetItem()
            self.item.setFont(self.font)
            self.item.setBackgroundColor(QtGui.QColor(200, 155, 255))

            self.idcImodTableWidget.setVerticalHeaderItem(i, self.item)
        self.idcImodTableWidget.resizeColumnsToContents()
        self.idcImodTableWidget.show()
        # self.idcImodTableWidget.clearContents()
        self.idcImodTableWidget.setHorizontalHeaderLabels(["Idc", "Imod"])
        self.idcImodTableWidget.setVerticalHeaderLabels(QtCore.QString("Ch0;Ch1;Ch2;Ch3").split(";"))
        'set data'
        for i in range(4):
            self.item = QtGui.QTableWidgetItem("70")
            self.item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.idcImodTableWidget.setItem(i, 0, self.item)
            self.item = QtGui.QTableWidgetItem("85")
            self.item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.idcImodTableWidget.setItem(i, 1, self.item)

        self.idcImodTableWidget.show()
        self.gridLayoutInsideTab2.addWidget(self.idcImodTableWidget, 3, 0, 1, 2)
        self.logger = QtGui.QTextEdit(self.gridLayoutWidgetInsideTab2)
        self.logger.setReadOnly(True)
        self.logger.setObjectName("logger")

        self.vecticalLayoutWidgetInsideTab2 = QtGui.QWidget(self.gridLayoutWidgetInsideTab2)
        self.vecticalLayoutInsideTab2 = QtGui.QVBoxLayout(self.vecticalLayoutWidgetInsideTab2)
        self.vecticalLayoutWidgetInsideTab2.setGeometry(10, 10, 30, 60)

        self.AAIDLbl = QtGui.QLabel(self.gridLayoutWidgetInsideTab2)
        self.AArateLbl = QtGui.QLabel(self.gridLayoutWidgetInsideTab2)
        self.AAIDLbl.setText("AA ID")
        self.AAIDLbl.setStyleSheet('color: blue')
        self.AAIDLbl.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))
        self.AArateLbl.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))
        self.AArateLbl.setStyleSheet('color: blue')
        self.AAIDLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.AArateLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.AArateLbl.setText("Rate Select")

        self.portID = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab2)

        self.lineEditAArate = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab2)
        self.portID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAArate.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayoutInsideTab2.addWidget(self.vecticalLayoutWidgetInsideTab2, 1, 2, 3, 1)
        self.gridLayoutInsideTab2.addWidget(self.logger, 2, 4, 2, 1)

        self.gridLayoutInsideTab2.addWidget(self.AArateLbl, 0, 0)
        self.gridLayoutInsideTab2.addWidget(self.AAIDLbl, 0, 1)
        self.gridLayoutInsideTab2.addWidget(self.lineEditAArate, 1, 0)
        self.gridLayoutInsideTab2.addWidget(self.portID, 1, 1)
        self.btnCh0 = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnCh1 = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnCh2 = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnCh3 = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnALLON = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnALLOFF = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnrdIdcImod = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnwdIdcImod = QtGui.QPushButton(self.vecticalLayoutWidgetInsideTab2)
        self.btnCh0.setText("Ch0 On")
        self.btnCh1.setText("Ch1 On")
        self.btnCh2.setText("Ch2 On")
        self.btnCh3.setText("Ch3 ON")
        self.btnALLON.setText("ALL ON")
        self.btnALLOFF.setText("ALL OFF")
        self.btnrdIdcImod.setText("Read IdcImod")
        self.btnwdIdcImod.setText("Write IdcImod")

        self.vecticalLayoutInsideTab2.addWidget(self.btnCh0)
        self.vecticalLayoutInsideTab2.addWidget(self.btnCh1)
        self.vecticalLayoutInsideTab2.addWidget(self.btnCh2)
        self.vecticalLayoutInsideTab2.addWidget(self.btnCh3)
        self.vecticalLayoutInsideTab2.addWidget(self.btnALLON)
        self.vecticalLayoutInsideTab2.addWidget(self.btnALLOFF)
        self.vecticalLayoutInsideTab2.addWidget(self.btnrdIdcImod)
        self.vecticalLayoutInsideTab2.addWidget(self.btnwdIdcImod)
        self.vecticalLayoutWidgetInsideTab2.show()

        self.tab2.setLayout(self.gridLayoutInsideTab2)
    def setupTab3GUI(self):
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(23)
        self.font1.setBold(True)
        self.font1.setWeight(20)
        self.font2 = QtGui.QFont()
        self.font2.setPointSize(15)
        self.font2.setBold(True)
        self.font2.setWeight(75)
        self.font3 = QtGui.QFont()
        self.font3.setPointSize(14)
        self.font3.setBold(True)
        self.font3.setWeight(75)

        self.gridLayoutWidgetInsideTab3 = QtGui.QWidget(self.tabWidget)
        self.tabWidget.setFont(self.font3)
        self.tabWidget.addTab(self.gridLayoutWidgetInsideTab3, "BER measurement")
        #self.tab3.setTitle("BER Measurement Display")
        #self.tabWidget.setGeometry(0, 0, 400, 300)


        #self.gridLayoutWidgetInsideTab3.setGeometry(0, 0, 200, 300)
        self.gridLayoutInsideTab3 = QtGui.QGridLayout(self.gridLayoutWidgetInsideTab3)
        #self.gridLayoutInsideTab3.addLayout()
        self.gridLayoutWidgetInsideTab3.setLayout(self.gridLayoutInsideTab3)
        #setStyleSheet("background-color:black;")
        # self.paletteGB=QtGui.QPalette()
        # self.paletteGB.setColor(QtGui.QPalette.Dark,QtCore.Qt.red)
        # self.tab3.setPalette(self.paletteGB)

        #USING LABEL QLABEL THE HEADING WILL HAVE SPREADOUT , PYQT4 PROBLEM
        self.btnBitErrorRate = QtGui.QPushButton("Bit Error Rate (BER)",self.gridLayoutWidgetInsideTab3)
        self.btnTotalErroCount = QtGui.QPushButton('Total No. of errors',self.gridLayoutWidgetInsideTab3)
        self.btnBitErrorRate.setStyleSheet("background-color:lightblue;\
            border: 0px solid #222222")
        self.btnTotalErroCount.setStyleSheet("background-color:lightblue;\
            border: 0px solid #222222")

        self.btnBitErrorRate.setFont(self.font1)
        self.btnTotalErroCount.setFont(self.font1)
        # self.lblBitErrorRate.setAlignment(QtCore.Qt.AlignCenter)
        # self.lblTotalError.setAlignment(QtCore.Qt.AlignCenter)
        # setting up the Channel label
        self.btnCh0=QtGui.QPushButton('Ch0',self.gridLayoutWidgetInsideTab3)
        self.btnCh1 = QtGui.QPushButton('Ch1', self.gridLayoutWidgetInsideTab3)
        self.btnCh2 = QtGui.QPushButton('Ch2', self.gridLayoutWidgetInsideTab3)
        self.btnCh3 = QtGui.QPushButton('Ch3', self.gridLayoutWidgetInsideTab3)

        w1=100
        self.btnCh0.setFixedWidth(w1)
        self.btnCh1.setFixedWidth(w1)
        self.btnCh2.setFixedWidth(w1)
        self.btnCh3.setFixedWidth(w1)
        self.btnCh0.setStyleSheet("background-color:lightblue;\
            border: 3px solid #222222")
        self.btnCh1.setStyleSheet("background-color:lightblue;\
            border: 3px solid #222222")
        self.btnCh2.setStyleSheet("background-color:lightblue;\
            border: 3px solid #222222")
        self.btnCh3.setStyleSheet("background-color:lightblue;\
            border: 3px solid #222222")
        self.btnCh0.setFont(self.font1)
        self.btnCh1.setFont(self.font1)
        self.btnCh2.setFont(self.font1)
        self.btnCh3.setFont(self.font1)
        # self.lblCh0 = QtGui.QLabel("Ch0")
        # self.lblCh1 = QtGui.QLabel("Ch1")
        # self.lblCh2 = QtGui.QLabel("Ch2")
        # self.lblCh3 = QtGui.QLabel("Ch3")
        #
        # self.lblCh0.setFont(self.font1)
        # self.lblCh1.setFont(self.font1)
        # self.lblCh2.setFont(self.font1)
        # self.lblCh3.setFont(self.font1)
        # self.lblCh0.setAlignment(QtCore.Qt.AlignCenter)
        # self.lblCh1.setAlignment(QtCore.Qt.AlignCenter)
        # self.lblCh2.setAlignment(QtCore.Qt.AlignCenter)
        # self.lblCh3.setAlignment(QtCore.Qt.AlignCenter)

        # fill = QtGui.QPixmap(23, )
        # fill.fill(QtCore.Qt.green)
        # self.lblCh0.setPixmap(fill)

        self.btnStartStopGating=PushButtonRight('Start Gating')
        self.btnStartStopGating.setFont(self.font2)
        self.btnInitBER=QtGui.QPushButton('Initialize',self.gridLayoutWidgetInsideTab3)
        self.btnInitBER.setFont(self.font2)
        self.btnInitBER.setFixedWidth(200)
        self.btnStartStopGating.setFixedWidth(200)
        #self.btnStartStopGating.adjustSize()


        self.slsetAttr =QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slsetAttr.setRange(1,50)
        # self.slsetAttr.setMinimum(1)
        # self.slsetAttr.setMaximum(25)
        self.slsetAttr.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slsetAttr.setTickInterval(0.5)
        self.slsetAttr.setSingleStep(1)
        self.slsetAttr.setPageStep(1)

        self.lblAttrValue = QtGui.QLabel('Set Attr. ' + str(self.slsetAttr.value()) + ' dB')
        self.lblAttrValue.setFont(self.font2)
        self.lblElapsedTime=QtGui.QLabel('Elapsed Time(s): ' )
        self.lblElapsedTime.setFont(self.font2)
        self.lblTransmitterBits = QtGui.QLabel('Transmitted Bits: ' )
        self.lblTransmitterBits.setFont(self.font2)
        self.lblDataRate = QtGui.QLabel('Data Rate:')
        self.lblDataRate.setFont(self.font2)
        self.txtElapsedTime=QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.txtTransmitterBits= QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.txtDataRate=QtGui.QLineEdit("25 Gbaud  OR 50 Gbps", self.gridLayoutWidgetInsideTab3)
        #self.txtDataRate2=QtGui.QLineEdit("50 Gbps", self.gridLayoutWidgetInsideTab3)
        self.txtElapsedTime.setAlignment(QtCore.Qt.AlignCenter)
        self.txtTransmitterBits.setAlignment(QtCore.Qt.AlignCenter)
        self.txtDataRate.setAlignment(QtCore.Qt.AlignCenter)
        #self.txtDataRate2.setAlignment(QtCore.Qt.AlignCenter)
        self.txtElapsedTime.setFixedWidth(w1*3.5)
        self.txtTransmitterBits.setFixedWidth(w1*3.5)
        self.txtDataRate.setFixedWidth(w1*3.5)
        #self.txtDataRate2.setFixedWidth(w1*1.5)


        # line edit box for all channel
        self.berCh0 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.berCh1 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.berCh2 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.berCh3 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)

        w = 280
        self.berCh0.setFont(self.font1)
        self.berCh1.setFont(self.font1)
        self.berCh2.setFont(self.font1)
        self.berCh3.setFont(self.font1)
        # self.berCh0.setFixedWidth(w)
        # self.berCh1.setFixedWidth(w)
        # self.berCh2.setFixedWidth(w)
        # self.berCh3.setFixedWidth(w)
        self.berCh0.setAlignment(QtCore.Qt.AlignCenter)
        self.berCh1.setAlignment(QtCore.Qt.AlignCenter)
        self.berCh2.setAlignment(QtCore.Qt.AlignCenter)
        self.berCh3.setAlignment(QtCore.Qt.AlignCenter)


        self.totalNoErrCh0 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.totalNoErrCh1 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.totalNoErrCh2 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.totalNoErrCh3 = QtGui.QLineEdit(self.gridLayoutWidgetInsideTab3)
        self.totalNoErrCh0.setFont(self.font1)
        self.totalNoErrCh1.setFont(self.font1)
        self.totalNoErrCh2.setFont(self.font1)
        self.totalNoErrCh3.setFont(self.font1)

        # self.totalNoErrCh0.setFixedWidth(w)
        # self.totalNoErrCh1.setFixedWidth(w)
        # self.totalNoErrCh2.setFixedWidth(w)
        # self.totalNoErrCh3.setFixedWidth(w)
        self.totalNoErrCh0.setAlignment(QtCore.Qt.AlignCenter)
        self.totalNoErrCh1.setAlignment(QtCore.Qt.AlignCenter)
        self.totalNoErrCh2.setAlignment(QtCore.Qt.AlignCenter)
        self.totalNoErrCh3.setAlignment(QtCore.Qt.AlignCenter)
        #self.frameDisplay=QtGui.QFrame(self.gridLayoutWidgetInsideTab3)
        self.palette = QtGui.QPalette()
        #self.palette.setBrush(QPalette.Background, QBrush(QtGui.QPixmap("C:\PAM4_GUI\logo.png")))
        self.pixmap1 = QtGui.QPixmap(os.getcwd()+"\logonew.png")
        self.kaiamLogo = QtGui.QLabel(self.gridLayoutWidgetInsideTab3)
       # self.kaiamLogo.setGeometry(0, 0, 30, 30)
       # self.kaiamLogo.setMargin(0)
        self.kaiamLogo.setPixmap(self.pixmap1)
        # self.palettePAM4 = QtGui.QPalette()
        # #self.palettePAM4.setBrush(QPalette.Background, QBrush(QtGui.QPixmap("C:\ROSA_Tester\Pam4.png")))
        # self.pixmap1PAM4 = QtGui.QPixmap("C:\ROSA_Tester\PAM4.png")
        # self.KaiamPAM4=QtGui.QLabel(self.gridLayoutWidgetInsideTab3)
        # self.KaiamPAM4.setPixmap(self.pixmap1PAM4)

        #self.kaiamLogo.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred );
        #self.kaiamLogo.setAutoFillBackground(True)
        self.gridLayoutInsideTab3.setSpacing(25)    #fine tuning the display as you want,global variable
        self.gridLayoutInsideTab3.addWidget(self.kaiamLogo, 0, 0,1,3)    # 0 row span, 3 column span
        #self.gridLayoutInsideTab3.addWidget(self.KaiamPAM4, 0, 2, 1, 1)  # 0 row span, 3 column span

        #self.gridLayoutInsideTab3.addWidget(self.lbldummy,0,0)
        self.gridLayoutInsideTab3.addWidget(self.btnBitErrorRate, 1, 1)
        self.gridLayoutInsideTab3.addWidget(self.btnTotalErroCount, 1,2)
        self.gridLayoutInsideTab3.addWidget(self.btnCh0, 2, 0)
        self.gridLayoutInsideTab3.addWidget(self.btnCh1, 3, 0)
        self.gridLayoutInsideTab3.addWidget(self.btnCh2, 4, 0)
        self.gridLayoutInsideTab3.addWidget(self.btnCh3, 5, 0)

        self.gridLayoutInsideTab3.addWidget(self.berCh0, 2, 1)
        self.gridLayoutInsideTab3.addWidget(self.berCh1, 3, 1)
        self.gridLayoutInsideTab3.addWidget(self.berCh2, 4, 1)
        self.gridLayoutInsideTab3.addWidget(self.berCh3, 5, 1)
        self.gridLayoutInsideTab3.addWidget(self.totalNoErrCh0, 2, 2)
        self.gridLayoutInsideTab3.addWidget(self.totalNoErrCh1, 3, 2)
        self.gridLayoutInsideTab3.addWidget(self.totalNoErrCh2, 4, 2)
        self.gridLayoutInsideTab3.addWidget(self.totalNoErrCh3, 5, 2)
        self.gridLayoutInsideTab3.addWidget(self.lblAttrValue,6,0,1,1)
        self.gridLayoutInsideTab3.addWidget(self.slsetAttr,6,1,1,2)
        self.gridLayoutInsideTab3.addWidget(self.lblElapsedTime,7,0)
        self.gridLayoutInsideTab3.addWidget(self.txtElapsedTime,7,1)
        self.gridLayoutInsideTab3.addWidget(self.lblTransmitterBits, 8, 0)
        self.gridLayoutInsideTab3.addWidget(self.txtTransmitterBits, 8, 1)
        self.gridLayoutInsideTab3.addWidget(self.lblDataRate, 9, 0)
        self.gridLayoutInsideTab3.addWidget(self.txtDataRate, 9, 1)


        self.gridLayoutInsideTab3.addWidget(self.btnStartStopGating,8,2,QtCore.Qt.AlignRight)
        self.gridLayoutInsideTab3.addWidget(self.btnInitBER, 9, 2,QtCore.Qt.AlignRight)


        #disable and enable some button state
        self.btnStartStopGatingState = False
        self.btnStartStopGating.setEnabled(self.btnStartStopGatingState)
        self.slsetAttr.setEnabled(False)
        self.btnInitBERState=False
        self.btnInitBER.setEnabled(not self.btnInitBERState)
        # self.gridLayoutWidgetInsideTab3.setPalette(self.palette)

        # self.kaiamLogo.setScaledContents(True)
        # set label
    def setupTab1GUISignalSlot(self):
        self.btneyeTest.clicked.connect(self.eyeCapture)
        self.btnloadPics.clicked.connect(self.loadImage)
        self.cbImagesType.currentIndexChanged.connect(self.cbImagesTypeSelectionChange)
        self.graphicsView_1.mouseDoubleClickEvent = self.loadIV_1
        self.graphicsView_2.mouseDoubleClickEvent = self.loadIV_2
        self.graphicsView_3.mouseDoubleClickEvent = self.loadIV_3
        self.graphicsView_4.mouseDoubleClickEvent = self.loadIV_4
    def setupTab2GUISignalSlot(self):

        self.idcImodTableWidget.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)
        self.btnrdIdcImod.clicked.connect(self.readQSFP28IdcImod)
        self.btnwdIdcImod.clicked.connect(self.writeQSFP28IdcImod)
        self.btnCh0.clicked.connect(self.setCh0OnOnly)
        self.btnCh1.clicked.connect(self.setCh1OnOnly)
        QtCore.QObject.connect(self.btnCh2, QtCore.SIGNAL("clicked()"), self.setCh2OnOnly)
        QtCore.QObject.connect(self.btnCh3, QtCore.SIGNAL("clicked()"), self.setCh3OnOnly)
        QtCore.QObject.connect(self.btnALLOFF, QtCore.SIGNAL("clicked()"), self.setALLChannelOFF)
        QtCore.QObject.connect(self.btnALLON, QtCore.SIGNAL("clicked()"), self.setALLChannelON)
    def setupTab3GUISignalSlot(self):
        # connect signal to method
        self.slsetAttr.valueChanged.connect(self.handleSliderAttrValueChange)
        self.btnInitBER.clicked.connect(self.handleInitButtonPressed)
        self.btnStartStopGating.clicked.connect(self.handleBTNStartGating)
        self.btnStartStopGating.rightClick.connect(self.openHiddenSettingDiagbox)

    def openHiddenSettingDiagbox(self):
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            if self.hiddenBERDialog1Flag:
                self.hiddenBERDialog1.hide()
                self.hiddenBERDialog1Flag=False
            else:
                self.hiddenBERDialog1.show()
                self.hiddenBERDialog1Flag=True

            print('Shift+Click' + "==>Open hidden diagbox to allow hidden selection")
    def setupTab3GUIHiddenDialog(self):
        dialog = QtGui.QDialog()
        bt1=QtGui.QPushButton('Test',dialog)
        dialog.show()


    def handleSliderAttrValueChange(self):
        if (self.main_ctrl.testBERMode !='Simulating'):
            self.main_ctrl.attrValueChange(self.getAttrSliderValue)
        else:
            self.main_ctrl.dummyTestAttrValueChange(self.getAttrSliderValue)

    # using property to set the GUI widget. consolidated one place to update all GUI indirectly from Model.py
    # and transferred calculated value from Ctrls.py
    def update_ui_from_model(self):
        self.getAttrSliderValue = self.model.changedValue
        self.runningCh0Err=self.model.Ch0totalError
        self.runningCh1Err = self.model.Ch1totalError
        self.runningCh2Err = self.model.Ch2totalError
        self.runningCh3Err = self.model.Ch3totalError
        self.runningCh0Ber=self.model.ch0BER
        self.runningCh1Ber=self.model.ch1BER
        self.runningCh2Ber = self.model.ch2BER
        self.runningCh3Ber = self.model.ch3BER
        self.runningTimeElapsed=self.model.timeElapsed
        self.runningTransmittedBit=self.model.transmittedBits

    def handleBTNStartGating(self):
        if (self.main_ctrl.testBERMode != 'Simulating'):
            if (self.btnStartStopGating.text() == "Start Gating"):
                # self.btnStartStopGatingState = True
                self.btnStartStopGating.setText("Stop Gating")
                self.main_ctrl.startGating()
            else:
                # self.btnStartStopGatingState = False
                self.btnStartStopGating.setText("Start Gating")
                self.main_ctrl.stopGating()

        else:
            #self.main_ctrl.dummyTestAttrValueChange(self.runningCh0Erro)
            if (self.btnStartStopGating.text() == "Start Gating"):
                # self.btnStartStopGatingState = True
                self.btnStartStopGating.setText("Stop Gating")
                self.main_ctrl.dummyTestGating()
            else:
                # self.btnStartStopGatingState = False
                self.btnStartStopGating.setText("Start Gating")
                self.main_ctrl.stopGating()

    def handleInitButtonPressed(self):

        #one button 2 roles and need to deal with different case
        if self.btnInitBER.text() == 'Initialize':
            # to do BER hardware initialization, reading config file, establish COM port and setup control parameter
            print('go to do setup control hardware parameters')
            if (self.main_ctrl.testBERMode !='Simulating'):
                if self.main_ctrl.openAttrCOMPort():
                    print( "Attenuator COM port open successfully and ready for use!")
                    newAttrValue = int(self.hiddenBERDialog1.ui.txtStartBerAttr_2.text())
                    self.main_ctrl.attrValueChange(newAttrValue*2)

                    self.slsetAttr.setValue(newAttrValue*2)
                    self.lblAttrValue.setText('Set Attr. ' + str(newAttrValue) + ' dB')
                    if self.main_ctrl.openQSFPddAAID():
                        print("QSFPdd AArdvark is open succesfully!")
                    else:
                        print("QSFPdd AArdvark is failed to connect!")
                        return False

                else:
                    print('Initialization hardware at attenuator COM port failed')
                    return False

            #handle button state sequence
            self.btnInitBER.setText("Release" if (self.btnInitBER.text() == 'Initialize' \
                                                  and not self.btnStartStopGating.isEnabled())  else "Initialize")
            self.btnStartStopGating.setEnabled(True if (self.btnInitBER.text() == 'Release') else False)
            self.btnStartStopGatingState = [True if (self.btnStartStopGating.isEnabled() and self.btnInitBER.text() == 'Initialize') else False]
            self.btnInitBERState = [True if self.btnStartStopGating.isEnabled() else False]
            self.slsetAttr.setEnabled(True)
            #otherwise
            #  Report error message and Stay the same
        elif self.btnInitBER.text() == 'Release':
            print('dealing with hardware release resource ')
            if (self.main_ctrl.testBERMode != 'Simulating'):
                self.main_ctrl.closeAttrCOMPort()
                self.main_ctrl.closeQSFPddAAID()
            self.btnInitBER.setText("Release" if (self.btnInitBER.text() == 'Initialize' \
                                                  and not self.btnStartStopGating.isEnabled())  else "Initialize")
            self.btnStartStopGating.setEnabled(True if (self.btnInitBER.text() == 'Release') else False)
            self.btnStartStopGatingState = [
                True if (self.btnStartStopGating.isEnabled() and self.btnInitBER.text() == 'Initialize') else False]
            self.btnStartStopGating.setText("Start Gating")    #consider some procedures to exit unexpected user interruption as needed,may need to add some code to handle
            self.btnInitBERState = [True if self.btnStartStopGating.isEnabled() else False]
            self.slsetAttr.setEnabled(False)
        else:
                pass



    def setupMainWindow(self):
        self.verticalLayoutWidget = QtGui.QWidget(self)
        self.verticalLayoutWidget.setGeometry(20, 10, 411, 411)
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)

        self.setWindowTitle("Kaiam PAM4 400Gbits Error Rate Measurement Control GUI")
        self.tabWidget = QtGui.QTabWidget(self.verticalLayoutWidget)

        self.tabWidget.setGeometry(10, 10, 411, 411)
        self.verticalLayout.addWidget(self.tabWidget)
        #self.setupTab1GUI()
        # self.setupTab2GUI()
        self.hiddenBERDialog1 = hiddenBERDialog()
        self.hiddenBERDialog1.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)
        self.hiddenBERDialog1.move(100, 100)
        self.hiddenBERDialog1Flag = False
        self.hiddenBERDialog1.ui.txtStartBerAttr_2.setText(str(self.main_ctrl.startBERAttr))
        self.hiddenBERDialog1.hide()

        self.setupTab3GUI()

        self.setLayout(self.verticalLayout)
        # setting flag
        self.waitWindowBox = None
        self.viewGraphEventAllow = False
        self.tabWidget.setCurrentIndex(0)
        self.setGeometry(0, 0, 700, 550)
        self.move(QtGui.QApplication.desktop().rect().center() - self.rect().center())

        self.show()
    def setupAllSignalsSlot(self):
        #self.setupTab1GUISignalSlot()
        #self.setupTab2GUISignalSlot()
        self.setupTab3GUISignalSlot()
    # def attrValueChange(self,value):
    #     size = float(value) /2  #self.slsetAttr.value()
    #
    #     #output=self.serialAttr.read()
    #     self.serialAttr.write("A"+ str(size)+'\r\n')
    #     sleep(1)
    #     print("Sending command A%.1f and set attenuator " %size)
    #     self.lblAttrValue.setText('Set Attr. ' + str(size) + ' dB')
    #     #elf.l1.setFont(QFont("Arial", size))


    # region hidden tab1 & tab2  (eye capture & module control disable/enable
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            self.hiddenBERDialog1.close()
        else:
            event.ignore()
def startGUI():
    app = QtGui.QApplication(sys.argv)
    initFileDirectory = "C:/ROSA_Tester/BER/"
    initFileName = "BER_InitFile_V100_SY.json"
    # BERControl = BERMesurement(initFileDirectory, initFileName)
    window = Window()
    return app.exec_()

if __name__ == '__main__':

    sys.exit(startGUI())
