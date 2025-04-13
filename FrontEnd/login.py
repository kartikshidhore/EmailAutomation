from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from api_client import login_user  
from dashboard import Dashboard
from signupPage import SignupPage 

class LoginWindow(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.email_label = QLabel("Email:", self)
        self.email_label.setStyleSheet("Color: white;")
        self.email_label.setFont(QFont("Arial", 20))
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Password:", self)
        self.password_label.setStyleSheet("Color: white;")
        self.password_label.setFont(QFont("Arial", 20))
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.authenticate)
        layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def authenticate(self):
        email = self.email_input.text()
        password = self.password_input.text()
        response = login_user(email, password)

        if response["status"] == "success":
            self.close()
            self.dashboard = Dashboard()
            self.dashboard.show()

    def signup(self):
        self.close()  # Close current window
        self.signup_window = SignupPage(self.main)
        self.signup_window.show()