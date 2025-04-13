from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from login import LoginWindow
from signupPage import SignupPage
from dashboard import Dashboard
from email_customizer import EmailCustomizer
import sys
class AppController:
    def __init__(self):
        self.login_window = None
        self.signup_window = None
        self.dashboard_window = None
        self.email_custom = None

    def show_login(self):
        # Only create if it doesn't exist
        if self.login_window is None:
            self.login_window = LoginWindow(main=self)

        if self.signup_window:
            self.signup_window.close()
            self.signup_window = None

        self.login_window.show()

    def show_signup(self):
        if self.signup_window is None:
            self.signup_window = SignupPage(main=self)

        if self.login_window:
            self.login_window.hide()

        self.signup_window.show()

    # def show_dashboard(self):
    #     if self.dashboard_window is None:
    #         self.dashboard_window = Dashboard(main=self)

    #     if self.email_custom:
    #         self.email_custom.close()

    #     self.dashboard_window.show()    

    # def show_emailCustomization(self):
    #     if self.email_custom is None:
    #         self.email_custom = EmailCustomizer(main=self)

    #     if self.dashboard_window:
    #         self.dashboard_window.hide()

    #     self.email_custom.show()             
            
app = QApplication(sys.argv)
window = AppController()
window.show_login()
sys.exit(app.exec())