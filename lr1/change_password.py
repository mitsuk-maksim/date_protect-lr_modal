# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_password.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChangePasswordWindow(object):
    def setupUi(self, ChangePasswordWindow):
        ChangePasswordWindow.setObjectName("ChangePasswordWindow")
        ChangePasswordWindow.resize(600, 333)
        self.centralwidget = QtWidgets.QWidget(ChangePasswordWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.newPasswordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.newPasswordEdit.setGeometry(QtCore.QRect(350, 30, 211, 31))
        self.newPasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPasswordEdit.setObjectName("newPasswordEdit")
        self.okButton = QtWidgets.QPushButton(self.centralwidget)
        self.okButton.setGeometry(QtCore.QRect(40, 220, 191, 41))
        self.okButton.setObjectName("okButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.confirmPasswordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.confirmPasswordEdit.setEnabled(True)
        self.confirmPasswordEdit.setGeometry(QtCore.QRect(350, 80, 211, 31))
        self.confirmPasswordEdit.setInputMask("")
        self.confirmPasswordEdit.setText("")
        self.confirmPasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasswordEdit.setObjectName("confirmPasswordEdit")
        self.errorPasswordLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorPasswordLabel.setGeometry(QtCore.QRect(210, 160, 321, 16))
        self.errorPasswordLabel.setText("")
        self.errorPasswordLabel.setObjectName("errorPasswordLabel")
        ChangePasswordWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ChangePasswordWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 18))
        self.menubar.setObjectName("menubar")
        ChangePasswordWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ChangePasswordWindow)
        self.statusbar.setObjectName("statusbar")
        ChangePasswordWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ChangePasswordWindow)
        QtCore.QMetaObject.connectSlotsByName(ChangePasswordWindow)

    def retranslateUi(self, ChangePasswordWindow):
        _translate = QtCore.QCoreApplication.translate
        ChangePasswordWindow.setWindowTitle(_translate("ChangePasswordWindow", "?????????? ????????????"))
        self.okButton.setText(_translate("ChangePasswordWindow", "Ok"))
        self.label.setText(_translate("ChangePasswordWindow", "?????????? ????????????"))
        self.label_2.setText(_translate("ChangePasswordWindow", "??????????????????????????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChangePasswordWindow = QtWidgets.QMainWindow()
    ui = Ui_ChangePasswordWindow()
    ui.setupUi(ChangePasswordWindow)
    ChangePasswordWindow.show()
    sys.exit(app.exec_())
