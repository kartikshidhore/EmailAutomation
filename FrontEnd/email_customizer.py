from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
)
import sys
import os
from dashboard import Dashboard


class EmailCustomizer(QMainWindow):
    def __init__(self, selected_users):
        super().__init__()
        # self.main = main
        self.setWindowTitle("Email Customizer")
        self.setGeometry(200, 100, 1000, 600)
        self.selected_users = selected_users
        self.attachments = []

        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        user_layout = QHBoxLayout()
        email_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Selected Users List
        self.user_list = QListWidget()
        for user in self.selected_users:
            name, email = user
            self.user_list.addItem(f"{name} <{email}>")
        user_layout.addWidget(QLabel("Recipients:"))
        user_layout.addWidget(self.user_list)

        # Email Text Edit
        self.email_edit = QTextEdit()
        self.email_edit.setPlaceholderText("Customize your email content here...")
        default_email_body = """
        <html>
        <body>
            <p>Dear [Name],</p>
            <p>This is a reminder for your upcoming training session.</p>
            <p>Best regards,<br>Your Team</p>
        </body>
        </html>
        """
        self.email_edit.setText(default_email_body)
        email_layout.addWidget(QLabel("Email Body:"))
        email_layout.addWidget(self.email_edit)

        # Buttons
        self.attach_button = QPushButton("Attach Files")
        self.attach_button.clicked.connect(self.add_attachment)

        self.send_button = QPushButton("Send Email")
        self.send_button.clicked.connect(self.send_email)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.attach_button)
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.back_button)

        # Combine all
        main_layout.addLayout(user_layout)
        main_layout.addLayout(email_layout)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_attachment(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "All Files (*);;PDF Files (*.pdf);;Images (*.png *.jpg *.jpeg)"
        )
        if files:
            self.attachments.extend(files)
            QMessageBox.information(self, "Files Attached", f"{len(files)} file(s) attached.")

    def send_email(self):
        body = self.email_edit.toPlainText()
        if not body.strip():
            QMessageBox.warning(self, "Empty Email", "Please write something in the email body.")
            return

        # For now, just simulate sending
        print("Sending email to:")
        for name, email in self.selected_users:
            print(f"- {name} <{email}>")

        print("Email content:")
        print(body)

        print("Attachments:")
        for file in self.attachments:
            print(f"- {file}")

        QMessageBox.information(self, "Success", "Emails sent successfully (simulation).")

    def go_back(self):
       
        self.close()
        self.show_dashboard = Dashboard()
        self.show_dashboard.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sample_users = [["Kartik Shidhore", "en21cs301367@medicaps.ac.in"], ["Shaunak Londhe", "shaunak443@gmail.com"]]
    window = EmailCustomizer(sample_users)
    window.show()
    sys.exit(app.exec())
