from flask import Flask, render_template

from forms import SignupForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data
        print(name, last_name, email, phone)
    return render_template("signup_form.html", form=form)
