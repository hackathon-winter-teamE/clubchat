from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re
from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

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
    clubs =  ['選択してください'] + dbConnect.getClubs()
    return render_template('registration/signup.html', club=clubs)

# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    club_name = request.form.get('clubs')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email =='' or password1 == '' or password2 == '' or club_name == '':
        flash('空のフォームがあります')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(email)
        club_id = dbConnect.getClubId(club_name)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(uid, name, email, password,club_id)
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


#channel 登録
@app.route('/ch', methods=['POST'])
def add_channel():
    print(uid)
    print(club_id)
    if uid is None:  #ユーザー登録がない場合ログイン画面にもどる
        return redirect('/login')
    channel_name = request.form.get('channnel-title')
    channnel = dbConnect.getChannelByName(name)
    club_id = dbConnect.getChannelByName(club_id)
    if channel == None:
        channel_description = request.form.get('channel-description')
        dbConnect.addChannel(uid,channel_name,channel_description,club_id)
        return redirect('/ch')
    else:
        error = '同じチャンネルが登録されています'
        return render_template('error/error.html',error_message=error)

#channel 削除
@app.route('/delete/<cid>')
def delete_channel(cid):
    uid = session.get("uid")
    print(uid)
    if uid is None:
        return redirect('/login')
    else:
        channel = dbconnect.getChannelByName(cid)
        print(channnel[uid] == uid)
        if channel["uid"]!=uid:
            flash('チャンネル作成者のみ削除可能です')
            return redirect('/')
        else:
            dbconnect.deleteChannel(cid)
            channnels = dbconnect.getChannelAll()
            return render_template('club.html',channels = channels,uid = uid)