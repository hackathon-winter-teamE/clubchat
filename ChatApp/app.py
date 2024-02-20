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
    return render_template('registration/test.html', clubs=clubs)

@app.route('/signup', methods=['POST'])
def userSignup():
    uid = uuid.uuid4()
    name = request.form.get('name') #ユーザー名
    email = request.form.get('email') #メールアドレス
    password1= request.form.get('password1') #パスワード1回目
    password2= request.form.get('password2') #パスワード確認用
    club= request.form.get('club') #部活名
    
    pattern = "^[a-zA-z0-9_.+-]+@[a-zA-Zo-9-]+\.[a-zA-Z0-9-.]+$"

    #入力された内容を確認する
    if name == '' or email=='' or password1 == '' or password2=='' or club=='':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('2つのパスワードが一致しません')
    elif re.match(pattern,email) is None:
        flash('メールアドレスが不正です')
    else:
    #DBに登録されていないことを確認
        password = hashlib.sha256(password1,encode('utf-8')).hexdigest()
        user = User(uid,name,email,password,club)  #clubが一致しなければOKなので部活変わっても問題ないはず
        DBuser = dbConnect.getUser(email)
    
        if DBuser!=None:
            flash('登録済みです')
        else:
            dbConnect.createUser(user)
            UserId = str(uid)
            session['uid'] = UserId
    return redirect('/signup')



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


# @app.route('/ch', methods=['POST'])
