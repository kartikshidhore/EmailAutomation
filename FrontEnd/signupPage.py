from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from api_client import LoginUser

class SignupPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.api = LoginUser()
        self.setWindowTitle("Sign Up")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.email_label = QLabel("Email:", self)
        self.email_label.setFont(QFont("Arial", 20))
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.password_label = QLabel("SMTP Password:", self)
        self.password_label.setFont(QFont("Arial", 20))
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("SMTP Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup)
        layout.addWidget(self.signup_button)

        self.login_link = QLabel('Already registered? <a href="#">Login here</a>')
        self.login_link.setOpenExternalLinks(False)
        self.login_link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.login_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_link.linkActivated.connect(self.redirectToLogin)
        layout.addWidget(self.login_link)

        self.setLayout(layout)

    def redirectToLogin(self):
        self.close()
        self.main.show_login()
    
    def signup(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        response = self.api.signup(email, password)

        if response is None:
            QMessageBox.warning(self, "Signup Failed", "Server error or unauthorized access.")
            return

        if response.get("status") == "success":
            QMessageBox.information(self, "Success", "Sign up successful!")
            self.close()
            self.main.show_login()
        else:
            QMessageBox.warning(self, "Signup Failed", response.get("message", "Signup failed."))

