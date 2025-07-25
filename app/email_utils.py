import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz
import yaml


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
timezone_str = config.get("timezone", "UTC")
try:
    user_timezone = pytz.timezone(timezone_str)
except pytz.UnknownTimeZoneError:
    print(f"⚠️ Unknown timezone '{timezone_str}' — falling back to UTC.")
    user_timezone = pytz.UTC

timestamp = datetime.now(user_timezone).strftime("%Y-%m-%d %H:%M %Z")

def send_job_matches_email(
    sender_email, sender_password, receiver_email, job_matches, keyword, summary_text=""
):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Your Daily Matched Job Postings for {keyword} – {timestamp}"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create HTML content
    # Start HTML content
    html = f"<h2>🔍 Matching Results for Keyword: {keyword}</h2>"
    for job in job_matches:
        html += f"""
        <hr>
        <p style='font-size:14px;'><b>✅ Match Score:</b> {job.get('score', 'N/A')}</p>
        <p style='font-size:14px;'><b>📝 Job Title:</b> {job['title']} at {job['employer']}</p>
        <p style='font-size:14px;'><b>🔗 URL:</b> 
            <a href="{job['url']}" style='font-size:12px;'>{job['url']}</a>
        </p>
        <p style='font-size:14px;'><b>💬 Reason:</b></p>
        <p style='font-size:14px;'>{job['reason']}</p>
        """

    if summary_text:
        html += "<hr><h3>📊 Summary</h3>"
        html += f"<div style='font-family:monospace; white-space:pre-wrap; font-size:14px;'>{summary_text}</div>"


    html += "<hr><p style='font-size:small;'>Generated by Smart Job Alerts</p>"
    message.attach(MIMEText(html, "html"))

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
