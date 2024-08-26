from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# التأكد من أن مجلد التحميل موجود
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    email = request.form['email']
    app_name = request.form['appName']
    files = request.files.getlist('websiteFiles')
    app_icon = request.files['appIcon']

    # حفظ الملفات المرفوعة في مجلد التحميلات
    for file in files:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    if app_icon:
        app_icon.save(os.path.join(app.config['UPLOAD_FOLDER'], app_icon.filename))

    # ضغط الملفات إلى ملف ZIP
    zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{app_name}.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            zipf.write(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), file.filename)
        if app_icon:
            zipf.write(os.path.join(app.config['UPLOAD_FOLDER'], app_icon.filename), app_icon.filename)

    # إعداد البريد الإلكتروني
    send_email_with_attachment(email, zip_filename)

    return 'تم إنشاء التطبيق وضغطه وإرساله عبر البريد الإلكتروني!'

def send_email_with_attachment(recipient_email, attachment_path):
    sender_email = "your-email@gmail.com"
    sender_password = "your-email-password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your App is Ready!"

    body = "Your app has been successfully created and is attached as a ZIP file."
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
        msg.attach(part)

    # إعداد الخادم وإرسال البريد الإلكتروني
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(loukmanehadjsaid210@gmail.com, hadjsaid210)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(debug=True)