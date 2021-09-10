import sys
import sqlite3
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

import entry
import change_password
import admin_mode


class CreateDB:
    db_conn = sqlite3.connect("date_protect.db")
    db_cursor = db_conn.cursor()
    db_cursor.execute("""CREATE TABLE if not exists users
                          (user_id integer primary key autoincrement,
                          username text NOT NULL unique, 
                          password text,
                          block integer DEFAULT 0,
                          extra_password integer DEFAULT 0,
                          is_superuser integer DEFAULT 0,
                          is_confirm integer DEFAULT 0)
                       """)
    try:
        db_cursor.execute("""
        insert into users(username, is_superuser) 
        values ('ADMIN', 1)
        """)
        db_conn.commit()
    except sqlite3.IntegrityError:
        pass


class Entry(QtWidgets.QMainWindow, entry.Ui_MainWindow, CreateDB):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.twoWindow = None
        self.okButton.clicked.connect(self.check)
        self.username = 'ADMIN'
        self.login_attempt = {
            'username': None,
            'count': 0
        }
        self.extra_password = False

    def check(self):
        username = self.nameEdit.text()
        password = self.passwordEdit.text()
        if not password:
            self.db_cursor.execute(f"""
            select username, password, is_confirm, block, extra_password, is_superuser from users
            where username = '{username}'
            """)
            result = self.db_cursor.fetchone()
            self.db_conn.commit()
            if result:
                is_confirm = result[2]
                block = result[3]
                extra_password = result[4]
                if not is_confirm:
                    if not block:
                        # смена пароля
                        self.twoWindow = ChangePassword()
                        self.twoWindow.show()
                        self.username = username
                        self.extra_password = True if extra_password else False
                        self.twoWindow.password[str].connect(self.set_new_password)
                    else:
                        self.errorPasswordLabel.setText("Вы заблокированы!")
                else:
                    self.errorPasswordLabel.setText('Запись уже подтверждена')
            else:
                self.errorPasswordLabel.setText("К сожалению, вы не администратор")
        else:
            self.db_cursor.execute(f"""
            select username from users
            where username = '{username}'
            """)
            result = self.db_cursor.fetchone()
            if not result:
                self.errorPasswordLabel.setText("К сожалению, учетной записи с таким именем не существует.")
                return

            if not self.login_attempt['username']:
                self.login_attempt['username'] = username

            self.db_cursor.execute(f"""
            select username, password, is_confirm, is_superuser, block, extra_password from users
            where username = '{username}' and password = '{password}'
            """)
            result = self.db_cursor.fetchone()
            if result:
                self.login_attempt = {
                    'username': None,
                    'count': 0
                }
                is_superuser = result[3]
                block = result[4]
                extra_password = result[5]
                if not is_superuser:
                    if not block:
                        self.twoWindow = ChangePassword()
                        self.twoWindow.show()
                        self.username = username
                        self.extra_password = True if extra_password else False
                        self.twoWindow.password[str].connect(self.set_new_password)
                    else:
                        self.errorPasswordLabel.setText("Вы заблокированы!")
                else:
                    # меню админа
                    self.twoWindow = AdminMode()
                    self.twoWindow.show()
            else:
                self.login_attempt['count'] += 1
                count = self.login_attempt['count']
                if count < 3:
                    self.errorPasswordLabel.setText(f"Неверный пароль. Осталось {3 - count} попыток")
                else:
                    self.errorPasswordLabel.setText("Завершнение работы.")
                    self.close()

    def set_new_password(self, password):
        if not self.extra_password:
            self.db_cursor.execute(f"""
            update users set password = '{password}', is_confirm = 1 where username = '{self.username}'
            """)
            self.db_conn.commit()
            self.errorPasswordLabel.setText('Пароль изменен')
            # self.close()
        else:
            print(password)
            if re.match(".*[A-Z].*", password) and re.match(".*[a-z].*", password) and re.match(".*[~!.......].*",
                                                                                                password):
                self.db_cursor.execute(f"""
                            update users set password = '{password}', is_confirm = 1 where username = '{self.username}'
                            """)
                self.db_conn.commit()
                self.errorPasswordLabel.setText('Пароль изменен')
                # self.close()
            else:
                self.errorPasswordLabel.setText('Пароль не соответствует специальным требованиям')


class ChangePassword(QtWidgets.QMainWindow, change_password.Ui_ChangePasswordWindow):
    password = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.okButton.clicked.connect(self.check)

    def check(self):
        if self.newPasswordEdit.text() == self.confirmPasswordEdit.text():
            self.password.emit(self.newPasswordEdit.text())
            self.close()
        else:
            self.errorPasswordLabel.setText('Пароли не совпадают')


class AdminMode(QtWidgets.QMainWindow, admin_mode.Ui_MainWindow, CreateDB):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.changePasswordButton.clicked.connect(self.change_password)

        self.db_cursor.execute(f"""
                    select username, block, extra_password from users
                    where is_superuser = 0
                    """)
        result = self.db_cursor.fetchall()
        self.db_conn.commit()
        for res in result:
            self.listWidget.addItem(res[0])
        self.listWidget.itemActivated.connect(self.item_activated_event)
        self.block = 0
        self.extra_password = 0
        self.username = None

        self.addUserButton.clicked.connect(self.add_user)
        # self.changeUserPermButton.clicked.connect(self.change_user_perm)

    def item_activated_event(self, item):
        self.db_cursor.execute(f"""
        select block, extra_password from users
        where username = '{item.text()}'
        """)
        self.username = item.text()
        result = self.db_cursor.fetchone()
        self.db_conn.commit()
        block = result[0]
        extra_password = result[1]
        self.blockCheckBox.setChecked(True if block else False)
        self.extraPasswordCheckBox.setChecked(True if extra_password else False)
        # после нажатия на чекбокс
        self.blockCheckBox.stateChanged.connect(self.change_block_perm)
        self.extraPasswordCheckBox.stateChanged.connect(self.change_extra_perm)

    def change_block_perm(self, state):
        print(self.username)
        block = 1 if state else 0
        self.db_cursor.execute(f"""
                update users set block = '{block}' where username = '{self.username}'
                """)
        self.db_conn.commit()

    def change_extra_perm(self, state):
        print(self.username)
        extra_password = 1 if state else 0
        self.db_cursor.execute(f"""
                update users set extra_password = '{extra_password}' where username = '{self.username}'
                """)
        self.db_conn.commit()

    def add_user(self):
        user = self.userLineEdit.text()
        try:
            self.db_cursor.execute(f"""
            insert into users(username)
            values ('{user}')
            """)
            self.db_conn.commit()
        except sqlite3.IntegrityError:
            pass
        self.userLineEdit.setText('')
        self.listWidget.addItem(user)

    def change_password(self):
        if self.newPasswordEdit.text() == self.confirmPasswordEdit.text():
            entry = Entry()
            entry.set_new_password(self.newPasswordEdit.text())
            self.close()
        else:
            self.errorPasswordLabel.setText('Пароли не совпадают')


def main():
    cdb = CreateDB()
    app = QtWidgets.QApplication(sys.argv)
    window = Entry()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

#
# import entry
# import dialog
#
# import sys
#
# app = entry.QtWidgets.QApplication(sys.argv)
# mainWindow = entry.QtWidgets.QMainWindow()
# ui = entry.Ui_mainWindow()
# ui.setupUi(mainWindow)
# mainWindow.show()
#
# def on_click():
#     entry.close()
#
# #
# ui.okButton.clicked.connect(on_click)
#
# sys.exit(app.exec_())
#
#
#
#
# # from PyQt5 import uic
# # from PyQt5.QtWidgets import QApplication
# #
# #
# # Form, Window = uic.loadUiType("entry.ui")
# # app = QApplication([])
# # window = Window()
# # form = Form()
# # form.setupUi(window)
# # window.show()
# #
# # def on_click():
# #     Form, Window = uic.loadUiType("dialog.ui")
# #     app = QApplication([])
# #     window = Window()
# #     form = Form()
# #     form.setupUi(window)
# #     window.show()
# #     # app.exec_()
# #
# #
# # form.okButton.clicked.connect(on_click)
# # app.exec_()
