from flask import Flask, render_template, url_for, request, flash, redirect
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

    if _check_current_password(username, oldpassword):
        _change_password(username, newpassword)
        flash('Your password have been changed.')
        return redirect(url_for('ask_credentials'))

    flash('Password mismatch. Check previous password')
    return render_template("credentials.html")

def _check_current_password(username, password):
    ht = HtpasswdFile("devel_users.passwd")
    return ht.check_password(username, password)

def _change_password(username, newpassword):
    ht = HtpasswdFile("devel_users.passwd")
    ht.set_password(username, newpassword)
    ht.save()

if __name__ == "__main__":
    app.debug = True
    app.run()
