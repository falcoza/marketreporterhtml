from data_fetcher import fetch_market_data
from infographic_generator import generate_html_infographic
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS, SMTP_SERVER, SMTP_PORT
from rss_generator import generate_rss_feed

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os


def send_email_report(html_content):
    print("Debug: EMAIL_SENDER =", EMAIL_SENDER)
    print("Debug: PASSWORD LOADED =", "Yes" if EMAIL_PASSWORD else "No")

    msg = MIMEMultipart("mixed")  # 'mixed' allows both HTML and attachments
    msg["Subject"] = "Market Report"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECEIVERS)

    # Attach the HTML body
    msg.attach(MIMEText(html_content, "html"))

    # Attach feed.xml as application/rss+xml
    try:
        with open("feed.xml", "rb") as xml_file:
            xml_data = xml_file.read()
            xml_attachment = MIMEApplication(xml_data, _subtype="rss+xml")
            xml_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename="market_report_feed.xml"
            )
            xml_attachment.add_header(
                'Content-Type',
                'application/rss+xml; charset=UTF-8'
            )
            msg.attach(xml_attachment)
            print("feed.xml attached successfully.")
    except Exception as e:
        print(f"Warning: Could not attach feed.xml - {e}")

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)
            server.starttls()
            print("Logging in to SMTP...")
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            print("Login successful. Sending email...")
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
            print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as auth_error:
        print("SMTP authentication failed:", auth_error)
    except Exception as e:
        print(f"Unexpected error during email send: {str(e)}")


def main():
    data = fetch_market_data()
    if not data:
        print("Failed to fetch market data.")
        return

    print("Market data fetched successfully.")
    html_content = generate_html_infographic(data)

    # Save HTML report
    with open("Market_Report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        print("HTML report saved as Market_Report.html")

    # Save RSS feed before sending
    generate_rss_feed(data)
    print("RSS feed saved as feed.xml")

    # Send email (with feed.xml attached)
    send_email_report(html_content)


if __name__ == "__main__":
    main()
