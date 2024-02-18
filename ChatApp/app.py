from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


@app.route('/')
def index():
    clubs = dbConnect.getClubsAll()
    return render_template('registration/signup.html', clubs=clubs)

@app.route('/', methods=['POST'])
def userSignup():
    uid = uuid.uuid4()
    user_name = request.form.get('name')
    email = request.form.get('email')
    password= request.form.get('password')
    club_id= request.form.get('club_id')
    dbConnect.createUser(uid,user_name, email, password,club_id)
    UserId = str(uid)
    session['uid'] = UserId
    return redirect('/')



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
