# HR Email Automation and Personalization System

🚀 A desktop application designed for HR departments to automate and personalize email communication with employees, built with Python PyQt6 frontend and Java Spring Boot backend.

---

## 🛠 Tech Stack

- **Frontend**: PyQt6 (Python)
- **Backend**: Spring Boot (Java)
- **Database**: H2 (Encrypted Local Database)
- **SMTP Server**: Gmail (App Password)
- **Authentication**: JWT Token based Secure API Access
- **API Testing**: Postman

---

## ✨ Features

- Secure Login and Signup with SMTP password (no extra login passwords)
- JWT Token generation and validation for all protected actions
- Import employee data from Excel files (.xlsx or .xls)
- Dynamic selection of recipients (single/multiple/select all)
- Rich-text Email customization with support for file attachments
- Bulk email sending via SMTP with authentication
- Local encrypted database storage (no internet required)
- H2 console for database inspection (for admins/devs)
- Error handling, validation, and user-friendly messaging

---

## 📦 Project Structure


---

## 🚀 How to Run

### Backend

1. Ensure you have Java 17+ and Maven installed.
2. Clone the repository.
3. Navigate to Backend folder.
4. Run:
    ```bash
    mvn spring-boot:run
    ```
5. Backend will start at `http://localhost:8080`

✅ APIs available for signup, login, and sending emails.

---

### Frontend

1. Install Python 3.10+.
2. Install dependencies:
    ```bash
    pip install pyqt6 pandas requests openpyxl
    ```
3. Navigate to Frontend folder.
4. Run:
   ```bash
   python main.py
   ```
    or
   ```bash
    python login.py
    ```

✅ Full Desktop Application ready for HR.

---

## 🔑 Important Notes

- You **must** use **Gmail App Passwords** (not your main Gmail password) for SMTP.
- `application.yml` should **not hardcode any real email/password** — users supply their own.
- JWT token is automatically stored after login and reused during session.
- The system is designed for intranet/internal deployment.

---

## 💻 API Endpoints Overview

| Endpoint | Method | Description |
|:---|:---|:---|
| `/api/auth/signup` | POST | Signup with email and SMTP password |
| `/api/auth/login` | POST | Login and receive JWT token |
| `/api/private/send-emails` | POST | Send bulk emails (JWT secured) |
| `/h2-console` | GET | Access H2 database console |

---

## 🤝 Contributions

Pull requests and feature suggestions are welcome!  
If you find a bug, feel free to create an issue.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developed and Maintained By

**Kartik Shidhore**

---

