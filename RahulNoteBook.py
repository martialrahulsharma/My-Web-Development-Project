from flask import Flask, render_template, redirect, request, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from random import randint
from flask_mail import Mail, Message
from validate_email import validate_email
import phonenumbers
import re
import razorpay
import json


# creates a object of Flask class
app = Flask(__name__)
#generate secrets keys
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
# creating databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

# flask mail configuration area start from
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yamrajiswaiting@gmail.com'
app.config['MAIL_PASSWORD'] = 'rahul@kt"";'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# instantiate the mail class
mail = Mail(app)
# Mail configuration area end here

login = LoginManager()
login.__init__(app)
login.login_view ='login'

db = SQLAlchemy(app)
db.init_app(app)
class Info(db.Model, UserMixin):
    otp = None
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    explain = db.Column(db.String(10000))
    example = db.Column(db.String(1000))

class User(db.Model, UserMixin):
    psw_return = None

    id = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(20))
    Last_name = db.Column(db.String(20))
    Email = db.Column(db.String(20), unique=True)
    Password = db.Column(db.String(20))
    Country = db.Column(db.String(20))
    Subject = db.Column(db.String(100))
    Date = db.Column(db.String(20))
    Phone_no = db.Column(db.String(20))

    # email validation method
    def email_validation(self,email):
        self.email_is_valid = validate_email(email, verify=True, check_mx=True)
        return self.email_is_valid

    # Phone number validation method
    def phone_validation(self, phone):
        my_number = phonenumbers.parse(phone, "IN")
        phone_is_valid = phonenumbers.is_valid_number(my_number)
        return phone_is_valid

    def pass_validation(self, password):
        User.psw_return = None
        if (len(password) < 8):
            return 'minimum 8 charactor should be'
        elif not re.search("[a-z]", password):
            return 'must be 1 lowercase characor'
        elif not re.search("[A-Z]", password):
            return 'must be 1 uppercase charactor '
        elif not re.search("[0-9]", password):
            return 'must be 1 number'
        elif not re.search("[_@$]", password):
            return 'must be spacial charactor _ or @ or $'
        elif re.search("\s", password):
            return 'password is weak'
        else:
            User.psw_return = True
            return 'Valid Password'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('home.html')
    # return render_template('A.html')

@app.route('/amount', methods=['POST','GET'])
def amount():
    if request.method == 'POST':
        amount = request.form.get('amount')
        return redirect(url_for('pay', amount=amount))
    return "Please check your input type"

@app.route('/pay/<amount>', methods=['POST','GET'])
def pay(amount):
    client = razorpay.Client(auth=("rzp_test_bDd8XQCTDHOdWe","lQu1fLZejCoTMQmpXtc0zDRe"))
    payment = client.order.create({'amount': (int(amount) * 100), 'currency': 'INR', 'payment_capture': '1'})
    return render_template('pay.html', payment=payment)

@app.route('/success', methods=['POST','GET'])
def success():
    return render_template('success.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/forgate_password')
def forgate_password():
    return render_template('forgate_password.html')

@app.route('/admin_profile')
@login_required
def admin_profile():
    return render_template('admin_profile.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# templating start from here
@app.route('/pythonIntroduction')
def Python_Introduction():
    return render_template('python_introduction.html')

@app.route('/python_module')
def Python_Module():
    return render_template('modul.html')

@app.route('/python_comment')
def Python_Comment():
    return render_template('comment.html')

@app.route('/python_string_slicing')
def Python_String_Slicing():
    return render_template('string_slicing.html')

@app.route('/python-list')
def Python_List():
    return render_template('python_list.html')

@app.route('/python-dictionary')
def Python_Dictionary():
    return render_template('dictionary_python.html')



@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/admin_profile')

    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(Email=email).first()
        if user:
            if check_password_hash(user.Password, request.form['passw']):
                login_user(user)
                return redirect('/admin_profile')

    return render_template('admin.html')

@app.route('/logout', methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('admin_profile'))

@app.route('/password_validation', methods=['POST','GET'])
def Password_Validation():
    if request.method == 'POST':
        password = request.form.get('psw')
        error = User.pass_validation(User, password)
        if User.psw_return == True:
            return jsonify({'msg':error})
        return jsonify({'error':error})

    return redirect('/signup')


# @app.route('/signup/submit', methods=['POST','GET'])
# def Signup():
#     if current_user.is_authenticated:
#         return redirect('/admin_profile')
#
#     if (request.method == 'POST'):
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         email_valid = User.email_validation(User,email)
#         if email_valid:
#             if User.query.filter_by(Email=email).first():
#                 msg = "Email already exist"
#                 return render_template("admin.html", msg=msg)
#
#             if User.phone_validation(User, phone):
#                 if User.psw_return == True:
#                     firstname = request.form.get('firstname')
#                     lastname = request.form.get('lastname')
#                     password = request.form.get('password')
#                     country = request.form.get('country')
#                     subject = request.form.get('subject')
#                     hash_passw = generate_password_hash(password)
#                     entry = User(First_Name = firstname, Last_name = lastname, Email = email, Password = hash_passw,
#                                      Country = country, Date = datetime.now(), Subject = subject, Phone_no = phone)
#                     db.session.add(entry)
#                     db.session.commit()
#                     return redirect('/admin')
#                 else:
#                     return "Please check your password field"
#             else:
#                 return "Invalid Phone number"
#         else:
#             return "Invalid username name"
#     return redirect('/signup')

@app.route('/signup/submit', methods=['POST','GET'])
def Signup():
    if current_user.is_authenticated:
        return redirect('/admin_profile')

    if (request.method == 'POST'):
        email = request.form.get('email')
        phone = request.form.get('phone')
        # email_valid = User.email_validation(User,email)
        # if email_valid:
        print(User.psw_return)
        if User.query.filter_by(Email=email).first():
            msg = "Email already exist"
            return render_template("admin.html", msg=msg)
        elif User.psw_return == True:
                print(User.psw_return)
                # if User.phone_validation(User, phone):
                firstname = request.form.get('firstname')
                lastname = request.form.get('lastname')
                password = request.form.get('password')
                country = request.form.get('country')
                subject = request.form.get('subject')
                hash_passw = generate_password_hash(password)
                entry = User(First_Name = firstname, Last_name = lastname, Email = email, Password = hash_passw,
                             Country = country, Date = datetime.now(), Subject = subject, Phone_no = phone)
                db.session.add(entry)
                db.session.commit()
                # User.psw_return = None
                return redirect('/admin')
        else:
                flash("Please check your Password field")
        # else:
        #         return "Invalid Phone number"
        # else:
        #     return "Invalid username name"

    return redirect('/signup')

@app.route('/forgate_password/sent_otp', methods=['POST', 'GET'])
def sent_otp():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(Email=email).first()
        if user:
            Info.otp = randint(1000, 9999)
            print(Info.otp)
            msg = Message('OTP', sender='yamrajiswaiting@gmail.com', recipients=[email])
            msg.body = str(Info.otp)
            mail.send(msg)
            return jsonify({'msg':'OTP has been send your registerd Email ID'})
    return jsonify({'error': 'Email not exist'})


@app.route('/forgate_password/validate_otp', methods=['POST', 'GET'])
def validate_otp():
    if request.method== 'POST':
        user_otp = request.form.get('OTP')
        if Info.otp == int(user_otp):
            return jsonify({'OTP':'OTP Veryfied'})
    return jsonify({'error':'OTP not matched'})

@app.route('/forgate_password/submit_password', methods=['POST','GET'])
def SubmitPassword():
    if request.method == 'POST':
        newps = request.form.get('newpsw')
        cnfps = request.form.get('cnfpsw')
        email = request.form.get('email')
        user = User.query.filter_by(Email=email).first()
        if (user) and (newps == cnfps):
            has_psw = generate_password_hash(newps)
            user.Password = has_psw
            db.session.commit()
            return redirect(url_for('admin'))
    return 'Password did not matched'

# admin/python coding starting here
@app.route('/study_python')
@login_required
def study_python():
    return render_template('py_intro.html')

@app.route('/contact/submit', methods=['POST','GET'])
def contact_submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        mesage = request.form.get('message')
        msg = Message(subject, sender=email, recipients=['martialrahulsharma@gmail.com'])
        msg.body = ("Name: " +name+ "\n" "Contact: " +phone+ "\n" "Subject: " +mesage)
        msg.html = render_template('home.html')
        mail.send(msg)
        return 'Form posted.'
    return render_template('contact.html')

@app.route("/python/submit", methods=['POST','GET'])
def python_submit():
    if request.method == 'POST':
        id = request.form.get('chapterid')
        titl = request.form.get('title')
        explai = request.form.get('explain')
        exampl = request.form.get('example')
        entry = Info(id=id, title=titl, explain=explai, example=exampl)
        db.session.add(entry)
        db.session.commit()
        return "successfuly send"

    return redirect(url_for('study_python'))

@app.route('/intro', methods=['POST','GET'])
def intro():
    print("hellklnl")
    if request.method == 'POST':
        print("hello")
        details = Info.query.all()
        print(details)
        return render_template('python_intro.html', details=details)
    return render_template('python_intro.html')



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000)