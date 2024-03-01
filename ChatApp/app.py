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
        # ログインユーザーのclub_idを取得
        user_club_id = dbConnect.getUserClubId(uid)
        # 取得したclub_idから所属している部活名を取得
        user_club_name = dbConnect.getUserClubName(user_club_id)
        # 取得したclub_idから所属している部活のチャンネル一覧を取得
        channels = dbConnect.getUserChannels(user_club_id)
        # 取得したチャンネルを新しい順に並べ替え
        if channels:
          channels.reverse()
    return render_template('index.html', user_club_name=user_club_name, channels=channels, uid=uid)

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    # フォームに入力されたデータを取得
    email = request.form.get('email')
    password = request.form.get('password')

    # 空のフォームがある場合
    if email =='' or password == '':
        flash('空のフォームがあります')
    # 空のフォームがない場合
    else:
        # 入力されたメールアドレスがDBにあるか照合
        user = dbConnect.getUser(email)
        # なかった場合
        if user is None:
            flash('このユーザーは存在しません')
        # あった場合
        else:
            # パスワード認証
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # 認証失敗
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            # 認証成功
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')

# サインアップページの表示
@app.route('/signup')
def signup():
    # DBから部活一覧を取得（フォームのリスト用）
    clubs = dbConnect.getClubs()
    return render_template('registration/signup.html', clubs=clubs)

# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    # フォームに入力されたデータを取得
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    selected_club_name = request.form.get('clubs')

    club_id = 0
    # 部活一覧を取得
    clubs = dbConnect.getClubs()

    # メールアドレスの形式を指定
    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # 空のフォームがある場合
    if name == '' or email =='' or password1 == '' or password2 == '' or selected_club_name == '':
        flash('空のフォームがあります')

    # パスワード確認
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')

    # メールアドレスの形式チェック
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')

    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(email)

        # すでに登録されていないか確認（DBにメールアドレスが有るか無いか）
        if DBuser != None:
            flash('既に登録されているようです')

        # フォームで選択した部活と同じ部活を部活一覧から探してIDをclub_idに代入
        else:
            for club in clubs:
                if club['club_name'] == selected_club_name:
                    club_id = club['club_id']

            # ユーザー登録
            dbConnect.createUser(uid, name, email, password, club_id)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
        
    return redirect('/signup')

# チャンネルの追加
@app.route('/', methods=['POST'])
def add_channel():
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')
    # フォームに入力されたチャンネル名を取得
    channel_name = request.form.get('channelTitle')
    # ログインユーザーのclub_idを取得
    user_club_id = dbConnect.getUserClubId(uid)
    # 入力されたチャンネル名と同じチャンネル名を取得
    # （ログインユーザーと同じclub_idのもののみ）
    channel = dbConnect.getChannelByName(channel_name,user_club_id)
    print(user_club_id)
    print(channel)
    # 重複が無い場合
    if channel == None :
        channel_description = request.form.get('channelDescription')
        dbConnect.addChannel(uid, channel_name, channel_description, user_club_id)
        return redirect('/')
    
    # 重複がある場合
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)
    
# チャンネルの更新
@app.route('/update_channel', methods=['POST'])
def update_channel():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = request.form.get('cid')
    channel_name = request.form.get('channelTitle')
    channel_description = request.form.get('channelDescription')

    dbConnect.updateChannel(uid, channel_name, channel_description, cid)
    return redirect('/detail/{cid}'.format(cid = cid))
    
# チャンネルの削除
@app.route('/delete/<cid>')
def delete_channel(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channel = dbConnect.getChannelById(cid)
        if channel["uid"] != uid:
            flash('チャンネルは作成者のみ削除可能です')
            return redirect ('/')
        else:
            dbConnect.deleteChannel(cid)
            return redirect('/')

# チャンネル詳細ページの表示
@app.route('/detail/<cid>')
def detail(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getChannelMessageAll(cid)
    replies = dbConnect.getReplyAll()
    print(replies)
    return render_template('detail.html', replies=replies, messages=messages, channel=channel, uid=uid)

#メッセージの投稿
@app.route('/message',methods=['POST'])
def add_message():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    
    message = request.form.get('newMessageForm')
    cid = request.form.get('cid')
    reply_id = request.form.get('reply-id')
    reply_user_name = request.form.get('reply_user_name')
    reply_message = request.form.get('reply_message')
    print(reply_id)
    print(reply_user_name)
    print(reply_message)
    if message:
        if reply_id:
            dbConnect.createMessage(uid, cid, message, reply_id)
            dbConnect.createReply(reply_user_name, reply_id, reply_message)
        else:
            dbConnect.createMessage(uid, cid, message, reply_id)
    
    return redirect('/detail/{cid}'.format(cid = cid))

#メッセージの削除
@app.route('/delete_message',methods=['POST'])
def delete_message():
    uid =session.get("uid")
    if uid is None:
        return redirect('/login')
    message_id = request.form.get('message_id')
    cid = request.form.get('cid')

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect('/detail/{cid}'.format(cid = cid))


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.errorhandler(404)
def show_error404(error):
    return render_template('error/404.html'),404


@app.errorhandler(500)
def show_error500(error):
    return render_template('error/500.html'),500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
