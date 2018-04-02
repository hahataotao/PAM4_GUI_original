# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BER_setting.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_setting(object):
    def setupUi(self, setting):
        setting.setObjectName(_fromUtf8("setting"))
        setting.resize(324, 258)
        self.gbBerSetting = QtGui.QGroupBox(setting)
        self.gbBerSetting.setGeometry(QtCore.QRect(19, 19, 291, 231))
        self.gbBerSetting.setObjectName(_fromUtf8("gbBerSetting"))
        self.gridLayoutWidget = QtGui.QWidget(self.gbBerSetting)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 281, 206))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridSettingLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridSettingLayout.setContentsMargins(5, -1, 4, 0)
        self.gridSettingLayout.setHorizontalSpacing(12)
        self.gridSettingLayout.setVerticalSpacing(7)
        self.gridSettingLayout.setObjectName(_fromUtf8("gridSettingLayout"))
        self.txtStartBerAttr_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtStartBerAttr_2.setAlignment(QtCore.Qt.AlignCenter)
        self.txtStartBerAttr_2.setObjectName(_fromUtf8("txtStartBerAttr_2"))
        self.gridSettingLayout.addWidget(self.txtStartBerAttr_2, 0, 1, 1, 1)
        self.lblEndBer = QtGui.QLabel(self.gridLayoutWidget)
        self.lblEndBer.setObjectName(_fromUtf8("lblEndBer"))
        self.gridSettingLayout.addWidget(self.lblEndBer, 1, 0, 1, 1)
        self.txtMinWaitTime = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtMinWaitTime.setAlignment(QtCore.Qt.AlignCenter)
        self.txtMinWaitTime.setObjectName(_fromUtf8("txtMinWaitTime"))
        self.gridSettingLayout.addWidget(self.txtMinWaitTime, 3, 1, 1, 1)
        self.txtEndBerAttr = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtEndBerAttr.setAlignment(QtCore.Qt.AlignCenter)
        self.txtEndBerAttr.setObjectName(_fromUtf8("txtEndBerAttr"))
        self.gridSettingLayout.addWidget(self.txtEndBerAttr, 1, 1, 1, 1)
        self.txtMaxWaitTime = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtMaxWaitTime.setAlignment(QtCore.Qt.AlignCenter)
        self.txtMaxWaitTime.setObjectName(_fromUtf8("txtMaxWaitTime"))
        self.gridSettingLayout.addWidget(self.txtMaxWaitTime, 4, 1, 1, 1)
        self.txtMinError = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtMinError.setAlignment(QtCore.Qt.AlignCenter)
        self.txtMinError.setObjectName(_fromUtf8("txtMinError"))
        self.gridSettingLayout.addWidget(self.txtMinError, 5, 1, 1, 1)
        self.lblEndBer_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.lblEndBer_3.setObjectName(_fromUtf8("lblEndBer_3"))
        self.gridSettingLayout.addWidget(self.lblEndBer_3, 4, 0, 1, 1)
        self.lblMinError = QtGui.QLabel(self.gridLayoutWidget)
        self.lblMinError.setObjectName(_fromUtf8("lblMinError"))
        self.gridSettingLayout.addWidget(self.lblMinError, 5, 0, 1, 1)
        self.lblAttrStep = QtGui.QLabel(self.gridLayoutWidget)
        self.lblAttrStep.setObjectName(_fromUtf8("lblAttrStep"))
        self.gridSettingLayout.addWidget(self.lblAttrStep, 2, 0, 1, 1)
        self.lblEndBer_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.lblEndBer_2.setObjectName(_fromUtf8("lblEndBer_2"))
        self.gridSettingLayout.addWidget(self.lblEndBer_2, 3, 0, 1, 1)
        self.txtAttrStep = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtAttrStep.setAlignment(QtCore.Qt.AlignCenter)
        self.txtAttrStep.setObjectName(_fromUtf8("txtAttrStep"))
        self.gridSettingLayout.addWidget(self.txtAttrStep, 2, 1, 1, 1)
        self.lblStartBer = QtGui.QLabel(self.gridLayoutWidget)
        self.lblStartBer.setObjectName(_fromUtf8("lblStartBer"))
        self.gridSettingLayout.addWidget(self.lblStartBer, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkBERLogging = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chkBERLogging.setObjectName(_fromUtf8("chkBERLogging"))
        self.verticalLayout.addWidget(self.chkBERLogging)
        self.chkBERLogging_2 = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chkBERLogging_2.setObjectName(_fromUtf8("chkBERLogging_2"))
        self.verticalLayout.addWidget(self.chkBERLogging_2)
        self.gridSettingLayout.addLayout(self.verticalLayout, 6, 1, 1, 1)
        self.lblTestSet = QtGui.QLabel(self.gridLayoutWidget)
        self.lblTestSet.setObjectName(_fromUtf8("lblTestSet"))
        self.gridSettingLayout.addWidget(self.lblTestSet, 6, 0, 1, 1)

        self.retranslateUi(setting)
        QtCore.QMetaObject.connectSlotsByName(setting)

    def retranslateUi(self, setting):
        setting.setWindowTitle(_translate("setting", "BER Setting", None))
        self.gbBerSetting.setTitle(_translate("setting", "Run Setting", None))
        self.lblEndBer.setText(_translate("setting", "End BER Attr:", None))
        self.lblEndBer_3.setText(_translate("setting", "Max. Ext. Wait Time:", None))
        self.lblMinError.setText(_translate("setting", "Min. Error:", None))
        self.lblAttrStep.setText(_translate("setting", "Attr Step", None))
        self.lblEndBer_2.setText(_translate("setting", "Min Ext. Wait Time:", None))
        self.lblStartBer.setText(_translate("setting", "Start BER Attr:", None))
        self.chkBERLogging.setText(_translate("setting", "Run BER Log Enable", None))
        self.chkBERLogging_2.setText(_translate("setting", "Long Term BER Enable", None))
        self.lblTestSet.setText(_translate("setting", "Test Logging Selection", None))

