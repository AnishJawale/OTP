from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y!@#123'  # Replace with your secret key

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'anish.jawale123@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'ixcinvmkjnjrdpof'           # Your App Password
app.config['MAIL_DEFAULT_SENDER'] = 'anish.jawale123@gmail.com'

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP
        session['otp'] = otp  # Store OTP in session
        session['email'] = email  # Store email in session
        
        msg = Message("Your OTP Code", recipients=[email])
        msg.body = f"Your OTP is {otp}"
        mail.send(msg)
        
        flash(f'An email with your OTP has been sent to {email}.', 'success')  # Flash message
        return redirect(url_for('otp'))
    return render_template('index.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if str(session.get('otp')) == entered_otp:
            flash('OTP verified successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    return render_template('otp.html')

if __name__ == '__main__':
    app.run(debug=True)
