from data_fetcher import fetch_market_data
from infographic_generator import generate_html_infographic
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS, SMTP_SERVER, SMTP_PORT

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def send_email_report(html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Market Report"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECEIVERS)

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())

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

    # Send email report
    try:
        send_email_report(html_content)
        print("HTML report emailed successfully.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    main()
