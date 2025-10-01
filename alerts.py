import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Alert
def send_email_alert(to_email, product_name, site, price, lowest_price, days):
    sender_email = "sravaniventra@gmail.com"
    sender_password = ""
    subject = f"Price Drop Alert  - {product_name}"
    body = f"""
    Good news! 🎉

    The product **{product_name}** on {site} has dropped to ₹{price:,}.
    This is the **lowest price in the last {days} days**  (previous lowest was ₹{lowest_price:,}).

    👉 Check it now before the price goes back up!
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False
