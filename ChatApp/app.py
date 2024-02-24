from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# チャンネル一覧ページの表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        user_club_id = dbConnect.getUserClubId(uid)
        user_club_name = dbConnect.getUserClubName(user_club_id)
        channels = dbConnect.getUserChannels(user_club_id)
        print(user_club_name)
        print(channels)
        if channels is None:
            return render_template('test.html')
    return render_template('index.html', user_club_name=user_club_name, channels=channels)

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあります')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')

# サインアップページの表示
@app.route('/signup')
def signup():
    clubs = dbConnect.getClubs()
    return render_template('registration/signup.html', clubs=clubs)

# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    selected_club_name = request.form.get('clubs')
    club_id = 0
    clubs = dbConnect.getClubs()

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email =='' or password1 == '' or password2 == '' or selected_club_name == '':
        flash('空のフォームがあります')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            for club in clubs:
                if club['club_name'] == selected_club_name:
                    club_id = club['club_id']

            dbConnect.createUser(uid, name, email, password, club_id)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')

# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
