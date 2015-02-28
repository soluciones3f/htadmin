from flask import Flask, render_template, url_for, request, flash, redirect, g, make_response, json, jsonify
from passlib.apache import HtpasswdFile
import xkcd_password

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

@app.route("/api/users", methods=["GET"])
def api_users_list():
    users = g.ht.users()
    response = make_response(json.dumps(users))
    response.headers['mimetype'] = 'application/json'
    return response

@app.route("/api/users/<username>", methods=["POST"])
def api_user_post(username):
    """Add user with random password only if user does not exists."""
    exists = g.ht.get_hash(username) == None
    if exists:
        password = _generate_password()
        g.ht.set_password(username, password)
        g.ht.save()
        return jsonify({'username': username, 'password': password})

    return jsonify({'error': 'username already exists'}), 409

@app.route("/api/users/<username>", methods=["DELETE"])
def api_user_delete(username):
    """Delete a user"""
    deleted = g.ht.delete(username)
    if deleted:
        g.ht.save()
        return jsonify({'username': username}), 200

    return jsonify({'error': "username does not exist"}), 404

@app.before_request
def before_request():
    g.ht = HtpasswdFile("devel_users.passwd")

def _generate_password():
    wordfile = xkcd_password.locate_wordfile()
    mywords = xkcd_password.generate_wordlist(wordfile=wordfile, min_length=4, max_length=8)
    return xkcd_password.generate_xkcdpassword(mywords, delim='-', n_words=3)

if __name__ == "__main__":
    app.debug = True
    app.run()
