from flask import Flask, render_template, request
import pandas as pd
import smtplib
import time
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_email():
    # CSVファイルを読み込む
    df = pd.read_csv('mail_list.csv')
    results = []

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            for _, row in df.iterrows():
                try:
                    msg = MIMEText(row['本文'])
                    msg['Subject'] = row['件名']
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = row['メールアドレス']

                    server.send_message(msg)
                    results.append(f"✅ Sent to: {row['メールアドレス']}")
                except Exception as e:
                    results.append(f"❌ Failed to send to {row['メールアドレス']}: {e}")
                time.sleep(1)

    except Exception as e:
        results.append(f"❌ SMTP connection error: {e}")

    return render_template('send_complete.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
