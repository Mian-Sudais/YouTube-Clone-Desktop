import os
import sys
import sqlite3
import smtplib
import ssl
import secrets
import hashlib
from datetime import datetime, timedelta
from email.message import EmailMessage

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


# Handle internal paths for bundled assets vs development scripts
if getattr(sys, "frozen", False):
    # Running as a bundled .exe: assets are extracted to a temporary runtime folder
    BASE_DIR = sys._MEIPASS
    # Database is stored outside the temp folder, right next to the executable
    DB_PATH = os.path.join(os.path.dirname(sys.executable), "users.db")
else:
    # Running normally as a local python script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "users.db")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "templates", "static"),
    static_url_path="/static",
)

# Securely baked inside the source code (will be encrypted via PyArmor)
app.secret_key = "miansudais-youtube-clone-super-secret-key-xyz776"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )

        # OTP-based password reset requests
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS password_reset_otps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                otp_hash TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                used INTEGER NOT NULL DEFAULT 0,
                attempts INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )


init_db()


def send_reset_otp_email(to_email: str, otp_code: str):
    host = "smtp-relay.brevo.com"
    port = 587
    username = "adb99f001@smtp-brevo.com"
    password = "NFdZrtUc9aILgyQM"
    mail_from = "miansudais776@gmail.com"  # your verified sender email

    msg = EmailMessage()
    msg["Subject"] = "Your password reset code"
    msg["From"] = mail_from
    msg["To"] = to_email
    msg.set_content(
        "Use this code to reset your password:\n\n"
        f"{otp_code}\n\n"
        "This code expires in 10 minutes.\n"
        "If this wasn't you, ignore this email."
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(username, password)
        server.send_message(msg)


def _now_utc_iso():
    return datetime.utcnow().isoformat()


@app.route("/")
def home():
    return redirect(url_for("signup"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("fullName", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirmPassword", "")

        if not full_name or not email or not password:
            return render_template("signup.html", error="Missing required fields.")
        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match.")

        pw_hash = generate_password_hash(password)

        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
                    (full_name, email, pw_hash),
                )
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Email already registered. Try logging in.")

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password")

        session["user_id"] = user["id"]
        session["email"] = user["email"]
        return redirect(url_for("youtubeclone"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Step 1: Request OTP
@app.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        try:
            with get_db() as conn:
                user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()

                # ONLY send OTP if this email exists
                if not user:
                    return render_template("forget.html", error="No account found with that email.")

                # Generate a secure 6-digit OTP
                otp = f"{secrets.randbelow(1_000_000):06d}"
                otp_hash = hashlib.sha256(otp.encode()).hexdigest()

                expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
                created_at = _now_utc_iso()

                # Invalidate previous unused OTPs for this user
                conn.execute(
                    "UPDATE password_reset_otps SET used = 1 WHERE user_id = ? AND used = 0",
                    (user["id"],),
                )

                conn.execute(
                    """
                    INSERT INTO password_reset_otps (user_id, otp_hash, expires_at, used, attempts, created_at)
                    VALUES (?, ?, ?, 0, 0, ?)
                    """,
                    (user["id"], otp_hash, expires_at, created_at),
                )

            # Send OTP email
            send_reset_otp_email(email, otp)

            # Go to verify screen
            return redirect(url_for("verify_otp", email=email))

        except Exception as e:
            return render_template("forget.html", error="An error occurred while sending the code. Please try again.")

    return render_template("forget.html")


# Step 2: Verify OTP
@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "GET":
        email = request.args.get("email", "").strip().lower()
        return render_template("verify_otp.html", email=email)

    email = request.form.get("email", "").strip().lower()
    otp = request.form.get("otp", "").strip()

    if not email or not otp or len(otp) != 6 or not otp.isdigit():
        return render_template("verify_otp.html", email=email, error="Enter the 6-digit code.")

    otp_hash = hashlib.sha256(otp.encode()).hexdigest()

    with get_db() as conn:
        user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            return render_template("verify_otp.html", email=email, error="Invalid code.")

        # Find matching OTP (latest unused)
        row = conn.execute(
            """
            SELECT * FROM password_reset_otps
            WHERE user_id = ? AND used = 0
            ORDER BY id DESC
            LIMIT 1
            """,
            (user["id"],),
        ).fetchone()

        if not row:
            return render_template("verify_otp.html", email=email, error="No active code. Request a new one.")

        if row["attempts"] >= 5:
            return render_template("verify_otp.html", email=email, error="Too many attempts. Request a new code.")

        if datetime.utcnow() > datetime.fromisoformat(row["expires_at"]):
            return render_template("verify_otp.html", email=email, error="Code expired. Request a new one.")

        # Wrong OTP -> increment attempts
        if otp_hash != row["otp_hash"]:
            conn.execute(
                "UPDATE password_reset_otps SET attempts = attempts + 1 WHERE id = ?",
                (row["id"],),
            )
            return render_template("verify_otp.html", email=email, error="Invalid code.")

        # Correct OTP -> mark used + allow reset in this session
        conn.execute("UPDATE password_reset_otps SET used = 1 WHERE id = ?", (row["id"],))

        session["reset_user_id"] = user["id"]
        session["reset_ok_until"] = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

    return redirect(url_for("reset_password_otp"))


# Step 3: Reset password (only after OTP verification)
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password_otp():
    uid = session.get("reset_user_id")
    until = session.get("reset_ok_until")

    if not uid or not until or datetime.utcnow() > datetime.fromisoformat(until):
        return redirect(url_for("forget"))

    if request.method == "POST":
        pw1 = request.form.get("password", "")
        pw2 = request.form.get("confirmPassword", "")

        if pw1 != pw2 or len(pw1) < 8:
            return render_template("reset.html", error="Passwords must match and be at least 8 characters.")

        with get_db() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (generate_password_hash(pw1), uid),
            )

        session.pop("reset_user_id", None)
        session.pop("reset_ok_until", None)

        return redirect(url_for("login"))

    return render_template("reset.html")


@app.route("/youtubeclone")
def youtubeclone():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("youtubeclone.html")


@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    import threading
    import webbrowser
    from waitress import serve

    host = "127.0.0.1"
    port = 5000
    url = f"http://{host}:{port}/"

    # Open browser shortly after server starts
    threading.Timer(1.0, lambda: webbrowser.open_new_tab(url)).start()

    # Production-style server
    serve(app, host=host, port=port)