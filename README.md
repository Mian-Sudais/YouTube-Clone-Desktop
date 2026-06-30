# 📺 YouTube Clone Desktop App

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0+-black?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Bootstrap-5.3.3-purple?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>A fully functional, standalone desktop recreation of the YouTube interface, built with Python (Flask) and Bootstrap 5, and packaged into a zero-dependency executable.</b>
</p>

---

## 🌟 Overview

This is a complete YouTube Clone application featuring user authentication, video browsing, and email-based password recovery. The app is packaged as a **single `.exe` file** using PyInstaller and protected with PyArmor, making it run natively on Windows without requiring Python installation, virtual environments, or manual setup.

---

## ✨ Features

### 🔐 User Authentication & Security
- **Secure Signup & Login**: User registration with Werkzeug password hashing.
- **Session Management**: Persistent and secure login sessions.
- **Email OTP Verification**: "Forgot Password" functionality with secure, time-sensitive One-Time Passwords sent via SMTP.
- **Code Obfuscation**: Backend logic is protected using **PyArmor** to prevent reverse engineering.

### 🎨 Modern YouTube-like UI
- **Responsive Design**: Built with **Bootstrap 5.3.3**, ensuring a clean, mobile-first layout.
- **YouTube Aesthetic**: Familiar interface with custom styling and smooth interactions.
- **Client-Side Validation**: Real-time form validation using vanilla JavaScript.

### 📺 Video Browsing & Search
- **Video Grid Display**: Browse videos across various categories (Tech, Cars, Nature, etc.).
- **Search Functionality**: Quickly find content using the integrated search bar.
- **Custom Video Player**: Dedicated HTML5 video playback interface.

### 📦 Zero-Dependency Desktop Execution
- **Standalone `.exe`**: Runs natively on Windows. No Python installation required.
- **Auto-Database Initialization**: Automatically creates a local `users.db` SQLite database on the first run.
- **Production Server**: Uses **Waitress** WSGI server for stable, production-grade local hosting.

---


## 🛠️ Tech Stack

| Category | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3.10+, Flask, Waitress (Production WSGI Server) |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3.3 |
| **Database** | SQLite3 (Local, auto-generated `users.db`) |
| **Security** | Werkzeug (Password Hashing), SMTPLib (Email OTP), PyArmor (Obfuscation) |
| **Packaging** | PyInstaller (Executable Bundling) |

---

## 📥 Download & Installation

Getting started is incredibly easy. You don't need to install Python or any dependencies!

1. **Download**: Go to the **[Releases](https://github.com/Mian-Sudais/YouTube-Clone-Desktop/releases)** section of this repository.
2. **Get the Executable**: Download the latest `YouTubeClone.exe` file.
3. **Run**: Double-click the `.exe` file to launch the application. *(No installation wizard needed!)*
4. **Browse**: Your default web browser will automatically open the app at `http://127.0.0.1:5000`.
5. **Data Storage**: The app will automatically generate a `users.db` file in the same directory to store your account data locally.

> **⚠️ Note:** 
> - An active internet connection is required for the **Email OTP (Forgot Password)** feature to connect to the SMTP server. 
> - Browsing and local authentication work perfectly offline.
> - It is recommended to place the `.exe` in its own dedicated folder, as it will generate the database file right next to it.

---

## 🛡️ Security & Privacy

- **Password Hashing**: Passwords are never stored in plain text. We use `werkzeug.security` to generate secure hashes.
- **Code Protection**: The distributed `.exe` is obfuscated using **PyArmor**, making it highly resistant to decompilation and reverse engineering.
- **Local Data**: All user data is stored locally in a SQLite database (`users.db`). No data is sent to external servers except for the SMTP email verification.

---

## 🐛 Troubleshooting

### **"Port 5000 already in use"**
- Close other applications using port 5000, or restart your computer.

### **"Email OTP not sending"**
- Ensure you have an active internet connection.
- The app uses a configured SMTP relay. If the developer's quota is exceeded, the OTP feature may temporarily fail. Local login and signup will still work.

### **Antivirus False Positive**
- Because the app is packaged with PyInstaller and obfuscated with PyArmor, some over-aggressive antivirus software might flag it as a false positive. The code is 100% safe and built by the developer.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Developer

**Sudais Ali Shah**  

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Mian-Sudais)

---

<p align="center">
  <b>If you found this project helpful, please consider giving it a ⭐ Star on GitHub!</b>
</p>

<p align="center">
  Made with ❤️ by Sudais Ali Shah
</p>
