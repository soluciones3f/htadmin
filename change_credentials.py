from flask import Flask, render_template, url_for, request, flash, redirect, g
from passlib.apache import HtpasswdFile

from string import ascii_letters, digits
from random import choice
from crypt import crypt

app = Flask(__name__)
app.secret_key = 'super dupper secret_mega_key'

@app.route("/")
def ask_credentials():
    return render_template("credentials.html")


@app.route("/", methods=["POST"])
def change_credential():
    username = request.form['username']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']

    if newpassword == "":
        flash("The new password can not be empty", 'warning')
        return render_template('credentials.html')

    if g.ht.check_password(username, oldpassword):
        g.ht.set_password(username, newpassword)
        g.ht.save()

        flash('Your password have been changed.', 'success')
        return redirect(url_for('ask_credentials'))

    flash('Password mismatch. Check previous password', 'danger')
    return render_template("credentials.html")

@app.before_request
def before_request():
    g.ht = HtpasswdFile("devel_users.passwd")

if __name__ == "__main__":
    app.debug = True
    app.run()
