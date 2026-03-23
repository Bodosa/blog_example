from flask import Flask, render_template, request
import smtplib
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_PASSWORD = os.getenv("OWN_PASSWORD")
posts = requests.get('https://api.npoint.io/674f5423f73deab1e9a7').json()


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


def send_email(name, email, phone, message):
    email_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    msg = MIMEText(email_message, "plain", "utf-8")
    msg["Subject"] = "New Message"
    msg["From"] = OWN_EMAIL
    msg["To"] = OWN_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.send_message(msg)


if __name__ == "__main__":
    app.run(debug=True)

