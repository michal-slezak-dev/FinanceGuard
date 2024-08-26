import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(username, message, user_email, from_email, to_email, smpt_pass):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # TLS

    msg = MIMEMultipart()
    msg['Subject'] = f"{username} - Contact Form Message"
    msg['From'] = from_email
    msg['To'] = to_email

    # attach the email content
    msg.attach(MIMEText(message + f"Message sent from {user_email}", 'plain'))

    try:
        connection = smtplib.SMTP(smtp_server, smtp_port)
        connection.starttls()  # secured connection

        connection.login(from_email, smpt_pass)
        connection.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.quit()
