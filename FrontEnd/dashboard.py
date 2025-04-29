import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QHeaderView,
    QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt
from email_customizer import EmailCustomizer
from api_client import LoginUser

class Dashboard(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client  # Save the API client with JWT token
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 1000, 600)

        self.data = None
        self.row_checkboxes = []

        self.layout = QVBoxLayout()

        self.upload_button = QPushButton("Upload Excel File")
        self.upload_button.clicked.connect(self.import_excel)
        self.layout.addWidget(self.upload_button)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.stateChanged.connect(self.select_all_clicked)
        self.layout.addWidget(self.select_all_checkbox)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.process_selected_rows)
        self.layout.addWidget(self.next_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            try:
                self.data = pd.read_excel(file_path)

                # Drop completely empty rows and columns
                self.data.dropna(axis=0, how='all', inplace=True)
                self.data.dropna(axis=1, how='all', inplace=True)

                # Drop unnamed columns
                self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed', case=False)]

                # Validate required columns
                required_cols = ['email', 'name']
                actual_cols = [col.strip().lower() for col in self.data.columns]

                if not any(col in actual_cols for col in ['email', 'emails', 'e-mails']):
                    raise ValueError("No 'Email' column found in Excel file.")

                if not any(col in actual_cols for col in ['name', 'names']):
                    raise ValueError("No 'Name' column found in Excel file.")

                self.populate_table()

            except Exception as e:
                QMessageBox.warning(self, "File Error", f"Error reading Excel file: {str(e)}")

    def populate_table(self):
        if self.data is None:
            return

        num_rows = len(self.data)
        num_cols = len(self.data.columns)
        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_cols + 1)  # +1 for checkbox
        self.table.setHorizontalHeaderLabels(["Select"] + list(self.data.columns))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.row_checkboxes.clear()

        for row_index in range(num_rows):
            checkbox = QCheckBox()
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row_index, 0, checkbox_widget)

            checkbox.stateChanged.connect(self.on_row_checkbox_changed)
            self.row_checkboxes.append(checkbox)

            for col_index in range(num_cols):
                item = QTableWidgetItem(str(self.data.iloc[row_index, col_index]))
                self.table.setItem(row_index, col_index + 1, item)

    def select_all_clicked(self):
        state = self.select_all_checkbox.isChecked()
        for checkbox in self.row_checkboxes:
            checkbox.setChecked(state)

    def on_row_checkbox_changed(self):
        all_checked = all(cb.isChecked() for cb in self.row_checkboxes)
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(all_checked)
        self.select_all_checkbox.blockSignals(False)

    def process_selected_rows(self):
        if self.data is None:
            QMessageBox.warning(self, "No Data", "Please upload an Excel file first.")
            return

        selected_users = []
        email_col_index = self.get_column_index('email')
        name_col_index = self.get_column_index('name')

        if email_col_index == -1 or name_col_index == -1:
            QMessageBox.warning(self, "Error", "Name or Email columns not found properly.")
            return

        for i, checkbox in enumerate(self.row_checkboxes):
            if checkbox.isChecked():
                name = self.table.item(i, name_col_index + 1).text()
                email = self.table.item(i, email_col_index + 1).text()
                selected_users.append((name, email))

        if not selected_users:
            QMessageBox.warning(self, "Selection Error", "No users selected.")
            return

        self.email_customizer = EmailCustomizer(self.api, selected_users)
        self.email_customizer.show()
        self.close()

    def get_column_index(self, search_key):
        for i, col in enumerate(self.data.columns):
            col_normalized = col.strip().lower().replace("-", "").replace("_", "")
            search_key_normalized = search_key.strip().lower().replace("-", "").replace("_", "")
            if search_key_normalized in col_normalized:
                return i
        return -1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    api = LoginUser()  # Normally login() would be called first
    window = Dashboard(api)
    window.show()
    sys.exit(app.exec())
