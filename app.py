from flask import Flask, render_template

from forms import SignupForm
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
        response = service.send_data()
        print(response)
    return render_template("signup_form.html", form=form)
