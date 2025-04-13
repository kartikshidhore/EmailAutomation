import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QHeaderView,
    QCheckBox, QAbstractItemView
)
from PyQt6.QtCore import Qt


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
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
                self.data.dropna(axis=0, how='all', inplace=True)  # Drop empty rows
                self.data.dropna(axis=1, how='all', inplace=True)  # Drop empty columns

                # Drop unnamed columns (e.g., "Unnamed: 3", "Unnamed: 4")
                self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]

                self.populate_table()
            except Exception as e:
                print("Error reading Excel file:", e)


    def populate_table(self):
        if self.data is None:
            return

        num_rows = len(self.data)
        num_cols = len(self.data.columns)
        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_cols + 1)  # +1 for checkbox column
        self.table.setHorizontalHeaderLabels(["Select"] + list(self.data.columns))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.row_checkboxes.clear()  # Reset previous checkboxes

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
        # Update "Select All" checkbox based on individual row states
        all_checked = all(cb.isChecked() for cb in self.row_checkboxes)
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(all_checked)
        self.select_all_checkbox.blockSignals(False)

    def process_selected_rows(self):
        selected_users = []
        for i, checkbox in enumerate(self.row_checkboxes):
            if checkbox.isChecked():
                row_data = [self.table.item(i, j).text() for j in range(1, self.table.columnCount())]
                selected_users.append(row_data)

        print("Selected Users:", selected_users)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())

# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
#     QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout,
#     QMessageBox, QAbstractItemView
# )
# from PyQt6.QtCore import Qt
# import pandas as pd
# # from email_customizer import EmailCustomizer

# class Dashboard(QWidget):
#     def __init__(self):
#         super().__init__()
#         # self.main = main
#         self.setWindowTitle("Dashboard")
#         self.setGeometry(200, 100, 1000, 600)

#         self.layout = QVBoxLayout(self)

#         self.upload_button = QPushButton("Upload Excel File")
#         self.upload_button.clicked.connect(self.import_excel)
#         self.layout.addWidget(self.upload_button)

#         self.select_all_checkbox = QCheckBox("Select All")
#         self.select_all_checkbox.stateChanged.connect(self.toggle_all_checkboxes)
#         self.layout.addWidget(self.select_all_checkbox)

#         self.table = QTableWidget()
#         self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
#         self.layout.addWidget(self.table)

#         self.next_button = QPushButton("Next")
#         self.next_button.clicked.connect(self.proceed_next)
#         self.layout.addWidget(self.next_button)

#         # Internal state
#         self.data = pd.DataFrame()
#         self.checkbox_refs = []
#         self.name_col = None
#         self.email_col = None

#     def import_excel(self):
#         file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
#         if not file_path:
#             return
#         try:
#             df = pd.read_excel(file_path)
#             df = df.astype(str).apply(lambda x: x.str.strip())

#             self.data = df.copy()
#             self.name_col, self.email_col = self.identify_columns(df.columns)

#             if not self.name_col or not self.email_col:
#                 raise ValueError("Could not detect 'Name' and 'Email' columns.")

#             self.populate_table()

#         except Exception as e:
#             QMessageBox.critical(self, "Error", str(e))

#     def identify_columns(self, columns):
#         name_keywords = ["name", "full name"]
#         email_keywords = ["email", "e-mail"]

#         name_col = None
#         email_col = None

#         for col in columns:
#             col_lower = col.lower()
#             if not name_col and any(keyword in col_lower for keyword in name_keywords):
#                 name_col = col
#             if not email_col and any(keyword in col_lower for keyword in email_keywords):
#                 email_col = col

#         return name_col, email_col

#     def populate_table(self):
#         df = self.data
#         self.table.setRowCount(len(df))
#         self.table.setColumnCount(len(df.columns) + 1)

#         headers = ["Select"] + list(df.columns)
#         self.table.setHorizontalHeaderLabels(headers)
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

#         self.checkbox_refs.clear()

#         for row in range(len(df)):
#             checkbox = QCheckBox()
#             self.table.setCellWidget(row, 0, checkbox)
#             self.checkbox_refs.append(checkbox)

#             for col in range(len(df.columns)):
#                 item = QTableWidgetItem(str(df.iat[row, col]))
#                 item.setFlags(Qt.ItemFlag.ItemIsEnabled)
#                 self.table.setItem(row, col + 1, item)

#     def toggle_all_checkboxes(self, state):
#         is_checked = state == Qt.CheckState.Checked
#         for checkbox in self.checkbox_refs:
#             checkbox.setChecked(is_checked)

#         self.table.viewport().update()

#     def proceed_next(self):
#         selected_users = []

#         for row, checkbox in enumerate(self.checkbox_refs):
#             if checkbox.isChecked():
#                 try:
#                     name = self.data.at[row, self.name_col].strip()
#                     email = self.data.at[row, self.email_col].strip()
#                     if name and email and email.lower() != "nan":
#                         selected_users.append([name, email])
#                 except Exception as e:
#                     print(f"Row {row} error: {e}")

#         print("Selected Users:", selected_users)
#         self.close()
#         # self.show_emailCustom = EmailCustomizer()
#         # self.show_emailCustom.show()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Dashboard()
#     window.show()
#     sys.exit(app.exec())


