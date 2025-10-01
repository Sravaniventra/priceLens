'''import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------------
# Send Email Alert
# -------------------------
def send_email_alert(to_email, product_name, site, price, lowest_price, days):
    sender_email = "yourgmail@gmail.com"
    sender_password = "your_app_password"  # 🔑 Use Gmail App Password, not real password!

    subject = f"Price Drop Alert 🚨 - {product_name}"
    body = f"""
    Good news! 🎉

    The product **{product_name}** on {site} has dropped to ₹{price:,}.
    This is the **lowest price in the last {days} days** (previous lowest was ₹{lowest_price:,}).

    👉 Check it now: Don't miss this deal!
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
        print("✅ Email sent successfully")
        return True
    except Exception as e:
        print("❌ Error sending email:", e)
        return False
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# -------------------------
# Send Email Alert
# -------------------------
def send_email_alert(to_email, product_name, site, price, lowest_price, days):
    """
    Sends a price drop alert email to the given recipient.

    Args:
        to_email (str): Recipient email address.
        product_name (str): Name of the product.
        site (str): Website (Amazon, Flipkart, etc.).
        price (float): Today's price.
        lowest_price (float): The lowest price in given days.
        days (int): The number of days for comparison.
    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    sender_email = "sravaniventrail@gmail.com"
    sender_password = "app_password"  #  Use Gmail App Password

    subject = f"🚨 Price Drop Alert - {product_name}"
    body = f"""
Good news! 🎉

The product **{product_name}** on {site} has dropped to ₹{price:,}.
This is the **lowest price in the last {days} days** (previous lowest was ₹{lowest_price:,}).

👉 Hurry! Don’t miss this deal.
"""

    # Build email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print("❌ Error sending email:", e)
        return False
