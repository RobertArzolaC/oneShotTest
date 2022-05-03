from flask import Flask, render_template, redirect, url_for, request

from forms import OtpFileForm, SignupForm, OtpForm
from services import OneShot


app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        surname_1 = form.surname_1.data
        surname_2 = form.surname_2.data
        email = form.email.data
        phone = form.phone.data

        service = OneShot()
        service.build_payload(name, surname_1, surname_2, email, phone)
        data_json = service.send_data()
        code = data_json['details']
        print("code: ", code)
        result = service.get_otp(code)

        if 'generated' in result['details']:
            return redirect(url_for('show_upload_file_form', code=code))
    return render_template("signup_form.html", form=form)


@app.route("/upload-otp-file/<code>/", methods=["GET", "POST"])
def show_upload_file_form(code):
    form = OtpFileForm()
    if form.validate_on_submit():
        upload_data = form.upload.data
        service = OneShot()
        response = service.upload_file(code, upload_data)
        if "200" in response['status']:
            document_id = response['details']
            return redirect(url_for('show_register_otp_form', code=code, document_id=document_id))
    return render_template("upload_file_otp.html", form=form)


@app.route("/register-otp/<code>/<document_id>", methods=["GET", "POST"])
def show_register_otp_form(code, document_id):
    form = OtpForm()
    if form.validate_on_submit():
        otp = form.otp.data
        service = OneShot()
        service.build_payload_otp(otp, document_id)
        result = service.send_otp(code)
        return result['details']
    return render_template("register_otp.html", form=form)
