from PyQt5.QtCore import *
from PyQt5.QtWidgets import QProgressBar, QDialog, QApplication
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import sqlite3
import re

db = sqlite3.connect("NIIT.db")
cur = db.cursor()
cur.execute('DROP TABLE IF EXISTS Student')
# cur.execute('''CREATE TABLE STUDENTS(RegNumber TEXT PRIMARY KEY UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL,
#                 Gender TEXT NOT NULL, DateOfBirth TEXT NOT NULL, Faculty TEXT NOT NULL, Department TEXT NOT NULL,CurrentLevel
#                  TEXT NOT NULL, Address TEXT NOT NULL, PhoneNumber TEXT UNIQUE, Status TEXT NOT NULL);''')

cur.execute('''
    CREATE TRIGGER IF NOT EXISTS Studentsmanager
     AFTER INSERT ON Students
     BEGIN
        UPDATE Students SET RegNumber = 'NIIT/2024/00'||(SELECT
        last_insert_rowid() FROM Students)
        WHERE rowid = new.rowid;
    END;
''')

# cur.execute('''CREATE TABLE STUDENTSStaff(StaffID TEXT PRIMARY KEY UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL,
#                 Gender TEXT NOT NULL, DateOfBirth TEXT NOT NULL, Faculty TEXT NOT NULL, Address TEXT MOT NULL, PhoneNumber TEXT UNIQUE,
#                 Email TEXT UNIQUE, Status TEXT NOT NULL);''')

cur.execute('''
    CREATE TRIGGER IF NOT EXISTS Staffmanager
     AFTER INSERT ON Students
     BEGIN
        UPDATE Staff SET StaffID = 'NIIT-EMP00'||(SELECT
        last_insert_rowid() FROM Staff)
        WHERE rowid = new.rowid;
    END;
''')
#
# cur.execute('''CREATE TABLE IF NOT EXISTS Admins(StaffID TEXT NOT NULL, FirstName TEXT NOT NULL, LastName TEXT NOT NULL,
#                Email TEXT UNIQUE, Password TEXT NOT NULL, FOREIGN KEY (StaffID) REFERENCES Staff(StaffID));
#                ''')

# cur.execute("INSERT into Admins (StaffID, FirstName, LastName,Email, Password) VALUES(?,?,?,?,?)",
#             ("NOO1","IFECHI","UDE","ifechiude@gmail.com","LEMONDROPS2.0"))
db.commit()
class NIITLoad(QDialog):
    def __init__(self, parent=None):
        super(NIITLoad, self).__init__(parent)
        loadUi("SIMLoadApp.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.progress = self.findChild(QProgressBar, "progressBar")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

    def update_progress(self):
        current_value = self.progress.value()

        if current_value < self.progress.maximum():
            self.progress.setValue(current_value + 5)

        else:
            self.timer.stop()
            self.close()
            # login_page = Login()
            # login_page.exec_()
            # login_page.show()
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login,self).__init__(parent)
        loadUi("SIMLoginPage.ui",self)
        self.loginbutton = self.findChild(QPushButton,"login_btn")
        self.username = self.findChild(QLineEdit,"user_ent")
        self.password = self.findChild(QLineEdit,"pass_ent")
        self.passworderror = self.findChild(QLabel,"userpass_err")
        self.secondwindow = AdminDash()
        self.secondwindow.hide()

        self.loginbutton.clicked.connect(self.gotonextpage)
        self.open()

    def gotonextpage(self):
        global username
        username = self.username.text().lower()
        password = self.password.text()
        username_regex = ("\S+@\S+\.[a-zA-Z]{2,}")
        password_regex = "^(?=.*[a-zA-Z0-9])(?=.*[\W_]).{8,}$"
        if re.match(password_regex,password) and re.match(username_regex,username):
            query = cur.execute(f'SELECT * FROM Admins WHERE E-mail="{username}" and Password="{password}"')
            if query.fetchall():
                query = cur.execute(f'SELECT FirstName, LastName FROM Admins WHWRE E-mail="{username}"')
                fullname = query.fetchall()
                for name, name2 in fullname:
                    x = "%s" % name
                    y = "&s" % name2
                    z = x + " " + y
                    self.secondwindow.namelabel.setText(z)
                self.secondwindow.displayadmindash()
                self.hide()
                admin_dash = AdminDash(self)
                admin_dash.exec_()
                admin_dash.show()
            else:
                self.passworderror.setText("Invalid Username or Password")
                self.username.setText(None)
                self.password.setText(None)
        else:
            self.passworderror.setText("Invalid Username or Password")
            self.username.setText(None)
            self.password.setText(None)
# 3 usages
class AdminDash(QDialog):
        def __init__(self,parent=None):
            super(AdminDash,self).__init__(parent)
            loadUi("SIMAdminDash.ui",self)
            self.logoutbutton = self.findChild(QPushButton,"logout_btn")
            self.menucombo = self.findChild(QComboBox,"menu_scroll")
            self.menubutton = self.findChild(QPushButton, "logout_btn")
            self.namelabel = self.findChild(QLabel,"user_name")

            self.logoutbutton.clicked.connect(self.logout)
            self.menubutton.clicked.connect(self.choosemenu)
            self.open

        def displaymaindash(self):
            self.show()
            self.exec_()
            self.hide()
            admin_dash = AdminDash()
            admin_dash.exec_()
            admin_dash.show()
        def choosemenu(self):
            if self.menucombo.currentText()=="Students":
                self.hide()
                # student_page = StudentsPage(self)
                # student_page.exec_()
                # student_page.show()
            elif self.menucombo.currentText()=="Admins":
                self.hide()
                admins_page = AdminPage()
                admins_page.exec_()
                admins_page.show
            elif self.menucombo.currentText()=="Staff":
                self.hide()
                # staff_page = StaffPage(self)
                # staff_page.exec_()
                # staff_page.show()
        def logout(self):
            self.hide
            login_page = Login(self)
            login_page.exec_()
            login_page.show()
class AdminPage(QDialog):
    def __init__(self,parent=None):
        super(AdminPage,self).__init__(parent)
        loadUi("SIMAdminPage.ui",self)
        self.backbutton = self.findChild(QPushButton, "back_btn")
        self.homebutton = self.findChild(QPushButton, "home_btn")
        self.logoutbutton = self.findChild(QPushButton, "logout_btn")
        self.regadmin = self.findChild(QPushButton, "reg_admin")
        self.listnumber = self.findChild(QSpinBox, "list_num")
        self.adminsearch = self.findChild(QComboBox, "admin_search")
        self.searchbar = self.findChild(QLineEdit, "searchbar")
        self.searchbutton = self.findChild(QPushButton, "search_btn")
        self.refreshbutton = self.findChild(QPushButton, "refresh_btn")
        self.editbutton = self.findChild(QPushButton, "edit_btn")
        self.deletebutton = self.findChild(QPushButton, "delete_btn")
        self.entries = self.findChild(QLabel, "entry_table")
        self.admintable = self.findChild(QTableWidget, "admin_table")

        query = cur.execute("SELECT * FROM Admins")
        result = query.fetchall()

        row = 0
        self.admintable.setRowCount(len(result))
        for person in result:
            self.admintable.setItem(row, 0, QTableWidgetItem(person[0]))
            self.admintable.setItem(row, 1, QTableWidgetItem(person[1]))
            self.admintable.setItem(row, 2, QTableWidgetItem(person[2]))
            self.admintable.setItem(row, 3, QTableWidgetItem(person[3]))
            row = row + 1
        self.entries.setText(f'showing{row} entries')

        self.backbutton.clicked.connect(self.gobacktoadmindash)
        self.homebutton.clicked.connect(self.gobacktoadmindash)
        self.logoutbutton.clicked.connect(self.gobacktologin)
        self.regadmin.clicked.connect(self.registeradmin)
        self.searchbutton.clicked.connect(self.searchadmin)
        self.refreshbutton.clicked.connect(self.refreshadmin)
        self.editbutton.clicked.connect(self.editadmin)
        self.deletebutton.clicked.connect(self.deleteadmin)

        self.open()

        def editadmin(self):
            self.hide()
            edit_admin = EditAdmin(self)
            edit_admin.exec_()
            edit_admin.show()

        def deleteadmin(self):
            self.hide()
            del_admin = DeleteAdmin(self)
            del_admin.exec_()
            del_admin.show()

        def refreshadmin(self):
            self.hide()
            ref_admin = AdminPage(self)
            ref_admin.exec_()
            ref_admin.show()

        def gobacktologin(self):
            self.hide()
            admin_dash = AdminDash()
            admin_dash.exec_()
            admin_dash.show()

        def registeradmin(self):
            self.hide()
            admin_reg = RegisterAdmin()
            admin_reg.exec_()
            admin_reg.show()

        def searchadmin(self):
            x = self.searchbar.text()
            if self.adminsearch.currentText()== "Staff ID":
                query = cur.execute(f'SELECT * FROM Admins WHERE StaffID = "{x}"')
            elif self.adminsearch.currentText() == "First Name":
                query = cur.execute(f'SELECT * FROM Admins WHERE FirstName = "{x}"')
            elif self.adminsearch.currentText() == "Email":
                query = cur.execute(f'SELECT * FROM Admins WHERE Email = "{x}"')
            result = query.fetchall()
            row = 0
            self.admintable.setRowCount(len(result))
            for person in result:
                self.admintable.setItem(row, 0, QTableWidget((person[0])))
                self.admintable.setItem(row, 1, QTableWidget((person[1])))
                self.admintable.setItem(row, 2, QTableWidget((person[2])))
                self.admintable.setItem(row, 3, QTableWidget((person[3])))
        row = row + 1
        self.entries.setText(f'showing{row} entries')

        self.searchbutton.clicked.connect(self.searchadmin)
class EditAdmin(QDialog):
    def __init__(self, parent=None):
        super(EditAdmin, self).__init__(parent)
        loadUi("SIMAdminEdit.ui", self)
        self.backbutton = self.findChild(QPushButton, "back_btn")
        self.homebutton = self.findChild(QPushButton, "home_btn")
        self.logoutbutton = self.findChild(QPushButton, "logout_btn")
        self.editoption = self.findChild(QComboBox, "edit_opt")
        self.oldadmin = self.findChild(QLineEdit, "admin_old")
        self.newadmin = self.findChild(QLineEdit, "admin_new")
        self.adminemail = self.findChild(QLineEdit, "admin_email")
        self.editbutton = self.findChild(QPushButton, "edit_btn")
        self.errorLabel = self.findChild(QLabel, "error_msg")

        self.backbutton.clicked.connect(self.gobacktoadminsdash)
        self.homebutton.clicked.connect(self.gobacktoadmindash)
        self.logoutbutton.clicked.connect(self.gobacktologin)
        self.editbutton.clicked.connect(self.editadmin)

        self.open()

    def gobacktoadminspage(self):
        self.hide()
        admin_page = AdminPage()
        admin_page.exec_()
        admin_page.show()

    def gobacktoadmindash(self):
        self.hide()
        admin_dash = AdminDash()
        admin_dash.exec_()
        admin_dash.show()

    def logout(self):
        self.hide()
        login_page = Login(self)
        login_page.show()

    def editadmin(self):
        admin = self.adminemail.text()
        new_info = self.newadmin.text()
        if self.editoption.currentText() == "Choose Edit Option":
            self.errorLabel.setText("\tChoose edit option")
        else:
            if self.editoption.currentText() == "Email":
                query = cur.execute(f'SELECT * FROM Admins WHERE Email = "{admin}"')
            if query.fetchall():
                cur.execute(f'UPDATE Admins SET Email = "{new_info}"WHERE Email = "{admin}"')
                db.commit()
                QMessageBox.information(self, "Success", "Admin edited succesfully")
                self.hide()
                admin_page = AdminPage(self)
                admin_page.exec_()
                admin_page.show()
            else:
                self.errorLabel.setText("User not found!")
                self.oldadmin.setText(None)
                self.newadmin.setText(None)
class DeleteAdmin(QDialog):
    def __init__(self, parent=None):
        super(DeleteAdmin, self).__init__(parent)
        loadUi("SIMAdminDel.ui", self)
        self.backbutton = self.findChild(QPushButton, "back_btn")
        self.homebutton = self.findChild(QPushButton, "home_btn")
        self.logoutbutton = self.findChild(QPushButton, "logoutbtn")
        self.deletetbutton = self.findChild(QPushButton, "del_opt")
        self.admininfo = self.findChild(QPushButton, "admin_info")
        self.deletebutton = self.findChild(QPushButton, "delete_btn")
        self.errorlabel = self.findChild(QPushButton, "error_msg")

        self.backbutton.clicked.connect(self.gobacktoadminspage)
        self.homebutton.clicked.connect(self.gobacktoadminspage)
        self.logoutbutton.clicked.connect(self.gobacktoadminspage)
        self.deletebutton.clicked.connect(self.gobacktoadminspage)

        self.open()

    def gobacktoadminspage(self):
        self.hide()
        admin_page = AdminPage()
        admin_page.exec_()
        admin_page.show()

    def gobacktoadmindash(self):
        self.hide()
        admin_dash = AdminDash()
        admin_dash.exec_()
        admin_dash.show()

    def logout(self):
        self.hide()
        login_page = Login(self)
        login_page.show()

    def deleteadmin(self):
        x = self.admininfo.text()
        new_info = self.newadmin.text()
        if self.deleteoption.currentText() == "Choose Delete Option":
            self.errorLabel.setText("Choose delete option")
        else:
            if self.deleteoption.currentText() == "Staff ID":
                query = cur.execute(f'SELECT * FROM Admins WHERE StaffID = "{x}"')
            if query.fetchall():
                cur.execute(f'DELETE FROM Admins WHERE StaffID = "{x}"')
                db.commit()
                QMessageBox.information(self, "Success", "Admin deleted succesfully")
                self.hide()
                admin_page = AdminPage(self)
                admin_page.exec_()
                admin_page.show()
            else:
                self.errorLabel.setText("User not found!")
                self.admininfo.setText(None)
class RegisterAdmin(QDialog):
    def __init__(self, parent=None):
        super(RegisterAdmin,self).__init__(parent)
        loadUi("SIMAdminRegPage.ui",self)
        self.staffId = self.findChild(QLineEdit,"staff_id")
        self.fname = self.findChild(QLineEdit,"staff_id")
        self.lname = self.findChild(QLineEdit,"staff_id")
        self.emailentry = self.findChild(QLineEdit,"staff_id")
        self.passWord = self.findChild(QLineEdit,"staff_id")
        self.confpass = self.findChild(QLineEdit,"staff_id")
        self.regbutton = self.findChild(QPushButton,"staff_id")
        self.findbutton = self.findChild(QPushButton,"staff_id")
        self.backbutton = self.findChild(QPushButton,"staff_id")
        self.logoutbutton = self.findChild(QPushButton,"staff_id")
        self.homebutton = self.findChild(QPushButton,"staff_id")
        self.errorlabel = self.findChild(QLabel,"staff_id")
        #go in and acc change those with the photos!

        self.regbutton.clicked.connect(self.adminregistration)
        self.backbutton.clicked.connect(self.gobacktoadminspage)
        self.homebutton.clicked.connect(self.gobacktoadmindash)
        self.findbutton.clicked.connect(self.findstaff)
        self.logoutbutton.clicked.connect(self.logout)

        self.open()

        def gobacktoadminspage(self):
            self.hide()
            admin_page = AdminPage()
            admin_page.exec_()
            admin_page.show()

        def gobacktoadmindash(self):
            self.hide()
            admin_dash = AdminDash()
            admin_dash.exec_()
            admin_dash.show()

        def logout(self):
            self.hide()
            login_page = Login(self)
            login_page.show()

        def findstaff(self):
            staffid = self.staffid.text()
            if staffid !="":
                query = cur.execute(f'SELECT StaffID FROM Staff WHERE StafdID = "{staffid}"')
                if query.fetchall():
                    query = cur.execute(f'SELECT FirstName FROM Staff WHERE StaffID = "{staffid}"')
                    firstname = query.fetchall()
                    for name in firstname:
                        self.fname.setText("%s" % name)
                    query=cur.execute(f'SELECT LastName FROM Staff WHERE StaffID = "{staffid}"')
                    lastname= query.fetchall()
                    for surname in lastname:
                        self.lname.setText("%s" % surname)
                    query=cur.execute(f'SELECT Email FROM Staff WHERE StaffID = "{staffid}"')
                    email = query.fetchall()
                    for email in email:
                        self.emailentry.setText("%s" % email)
                else:
                    self.errorLabel.setText("Staff not found!")
            else:
                self.errorLabel.setText("Insert Staff ID and Find Staff")

        def adminregistration(self):
            staffid = self.staffId.text()
            firstName = self.fname.text().capitalize()
            lastName = self.lname.text().capitalize()
            email = self.emailentry.text().lower()
            password = self.passWord.text()
            confirm = self.confpass.text()
            email_regex = re.compile(r'([A-Za-z0-9]+[.-_]*[A-Za-z0-9]+[A-Z|a-z]{2})')
            password_regex = r"^(?=.*\d)(?=.[a-z])(?=*[A-Z])'{8,}"

            if firstName!="" or lastName!=""or email !="" or password !="":
                if password != confirm:
                    self.erroLabel.setText("Passwords do not match")
                elif not re.match(password_regex, password):
                    self.erroLabel.setText("Password must contain at least\n\ta lowercase\n\tan uppercase\n\ta number\n\ta special "
                                           "character\n\tand must not be less than 8 characters")
                    self.passWord.setText(None)
                    self.confpass.setText(None)
                elif not re.match(email_regex, email):
                    self.erroLabel.setText("Invalid Email")
                    self.emailentry.setText(None)
                    self.passWord.setText(None)
                    self.confpass.setText(None)
                else:
                    try:
                        cur.execute("INSERT INTO Admins(StaffID, FirstName, LastName, Password, Email) VALUES(?,?,?,?,?)"
                                    , (staffid, firstName, lastName, password, email))
                        db.commit()
                        QMessageBox.information(self, "Success", "Admin registration successful!")
                        self.hide()
                        reg_admin = RegisterAdmin(self)
                        reg_admin.exec_()
                        reg_admin.show()

                    except sqlite3.IntergityError:
                        self.errorLabel.setText("Email already exists")
            else:
                self.errorLabel.setText("insert Staff ID and Find staff")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Load_Screen = NIITLoad()
    Load_Screen.exec_()
    sys.exit(app.exec_())