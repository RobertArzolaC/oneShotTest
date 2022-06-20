from flask import Flask, render_template, redirect, url_for, session

from forms import OtpFileForm, SignupForm, OtpForm, SignInForm, SetCodeForm

from services import OneShot


app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"


@app.route("/", methods=["GET", "POST"])
def show_sign_in_form():
    form = SignInForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        session["password"] = form.password.data
        return redirect(url_for("show_set_code"))
    return render_template("login.html", form=form)


@app.route("/set-code", methods=["GET", "POST"])
def show_set_code():
    form = SetCodeForm()
    if form.validate_on_submit():
        session["code"] = form.code.data
        return redirect(url_for("show_signup_form"))
    return render_template("set_code.html", form=form)


@app.route("/sign-up", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        surname_1 = form.surname_1.data
        surname_2 = form.surname_2.data
        email = form.email.data
        phone = form.phone.data

        service = OneShot()
        service.build_payload(
            name,
            surname_1,
            surname_2,
            email,
            phone,
            session.get("username"),
            session.get("password"),
            session.get("code"),
        )
        data_json = service.send_data()
        if not data_json:
            return render_template(
                "error_server.html", error_json=service.payload
            )

        code = data_json["details"]
        result = service.get_otp(code)
        if "generated" in result["details"]:
            return redirect(url_for("show_upload_file_form", code=code))
    return render_template("signup_form.html", form=form)


@app.route("/upload-otp-file/<code>/", methods=["GET", "POST"])
def show_upload_file_form(code):
    form = OtpFileForm()
    if form.validate_on_submit():
        upload_data = form.upload.data
        service = OneShot()
        response = service.upload_file(code, upload_data)
        if "200" in response["status"]:
            document_id = response["details"]
            return redirect(
                url_for(
                    "show_register_otp_form",
                    code=code,
                    document_id=document_id,
                )
            )
    return render_template("upload_file_otp.html", form=form)


@app.route("/register-otp/<code>/<document_id>", methods=["GET", "POST"])
def show_register_otp_form(code, document_id):
    form = OtpForm()
    if form.validate_on_submit():
        otp = form.otp.data
        service = OneShot()
        service.build_payload_otp(otp, document_id)
        result = service.send_otp(code)
        if "200" in result["status"]:
            return redirect(
                url_for(
                    "show_download_otp_form",
                    code=code,
                    document_id=document_id,
                )
            )
    return render_template("register_otp.html", form=form)


@app.route("/download-otp/<code>/<document_id>", methods=["GET", "POST"])
def show_download_otp_form(code, document_id):
    service = OneShot()
    url_dowload_file = service.get_download_file_url(code, document_id)
    return render_template("download_otp.html", link_file=url_dowload_file)
