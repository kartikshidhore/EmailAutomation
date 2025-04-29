from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QMessageBox
)
import sys
import os

class EmailCustomizer(QMainWindow):
    def __init__(self, api, selected_users):
        super().__init__()
        self.api = api
        self.selected_users = selected_users
        self.attachments = []
        self.setWindowTitle("Email Customizer")
        self.setGeometry(200, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        user_layout = QHBoxLayout()
        email_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.user_list = QListWidget()
        for user in self.selected_users:
            name, email = user
            self.user_list.addItem(f"{name} <{email}>")
        user_layout.addWidget(QLabel("Recipients:"))
        user_layout.addWidget(self.user_list)

        self.email_edit = QTextEdit()
        self.email_edit.setPlaceholderText("Customize your email content here...")
        email_layout.addWidget(QLabel("Email Body:"))
        email_layout.addWidget(self.email_edit)

        self.attach_button = QPushButton("Attach Files")
        self.attach_button.clicked.connect(self.add_attachment)

        self.send_button = QPushButton("Send Email")
        self.send_button.clicked.connect(self.send_email)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.attach_button)
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.back_button)

        main_layout.addLayout(user_layout)
        main_layout.addLayout(email_layout)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_attachment(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        if files:
            self.attachments.extend(files)
            QMessageBox.information(self, "Files Attached", f"{len(files)} file(s) attached.")

    def send_email(self):
        body = self.email_edit.toHtml()
        if not body.strip():
            QMessageBox.warning(self, "Empty Email", "Please write something in the email body.")
            return

        recipients = []
        for name, email in self.selected_users:
            recipients.append({
                "name": name,
                "email": email
            })

        attachments_data = []
        for filepath in self.attachments:
            with open(filepath, "rb") as f:
                file_content = f.read()
                attachments_data.append({
                    "filename": os.path.basename(filepath),
                    "filedata": file_content.hex()
                })

        email_payload = {
            "subject": "Customized Subject",
            "body": body,
            "recipients": recipients,
            "attachments": attachments_data
        }

        response = self.api.send_email_with_attachments(email_payload)

        if response and response.get("status") == "success":
            QMessageBox.information(self, "Success", "Emails sent successfully!")
        else:
            QMessageBox.warning(self, "Error", response.get("message", "Failed to send emails."))

    def go_back(self):
        from dashboard import Dashboard
        self.close()
        self.dashboard = Dashboard(self.api)
        self.dashboard.show()
         
