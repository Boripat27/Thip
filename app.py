from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

# โหลดค่าจาก .env
load_dotenv()

app = Flask(__name__)

# ตั้งค่าโฟลเดอร์สำหรับอัปโหลดรูป
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ตั้งค่าการใช้งาน Gmail สำหรับส่งอีเมล
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# หน้าแรก
@app.route('/')
def index():
    return render_template('index.html')

# หน้าเกี่ยวกับ
@app.route('/about')
def about():
    return render_template('about.html')

# หน้าแกลลอรี่ (แสดงรูป)
@app.route('/gallery')
def gallery():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', images=images)

# หน้าอัปโหลดรูป
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('gallery'))
    return render_template('upload.html')

# หน้า Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(f'📬 ข้อความจาก {name}',
                      sender=email,
                      recipients=[os.getenv('MAIL_USERNAME')])
        msg.body = f'ชื่อ: {name}\nอีเมล: {email}\n\nข้อความ:\n{message}'
        mail.send(msg)

        return render_template('contact.html', success=True)

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
