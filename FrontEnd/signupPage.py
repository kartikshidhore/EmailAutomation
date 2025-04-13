from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from api_client import login_user  

class SignupPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 400, 200)
        self.main = main

        layout = QVBoxLayout()
        self.textLabel = QLabel("Enter valid Email and Password!", self)
        
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

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup)
        layout.addWidget(self.signup_button)

        self.login_link = QLabel('Already registered? <a href="#">Login here</a>')
        self.login_link.setOpenExternalLinks(False)  # We handle the click ourselves
        self.login_link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.login_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.login_link.linkActivated.connect(self.redirectToLogin)

        layout.addWidget(self.login_link)
        self.setLayout(layout)

    def redirectToLogin(self):
        # Logic to redirect to the login page
        print("Redirecting to Login Page...")
        self.close()  # Close current window
        self.main.show_login()  # Show login window

    def signup(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        # Call the API to sign up the user
        response = login_user(email, password)
        if response['status'] == 'success':
            QMessageBox.information(self, "Success", "Sign up successful!")
            self.close()
            self.main.show_login()
        else:
            QMessageBox.warning(self, "Error", response['message'])