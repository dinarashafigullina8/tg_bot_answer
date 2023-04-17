import smtplib
import os
from email.mime.text import MIMEText


def send_email(message):
    sender = os.getenv('email_from')
    password = os.getenv('email_password')

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = 'Новый вопрос'
        server.sendmail(sender, sender, msg.as_string())
        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    message = 'Пришел новый вопрос. Пожалуйста зайдите в группу операторов'
    print(send_email(message=message))


if __name__ == "__main__":
    main()
