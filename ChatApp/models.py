import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
    # ユーザー登録
    def createUser(uid, user_name, email, password,club_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql="INSERT INTO users (uid,user_name, email, password,club_id) VALUES (%s, %s, %s, %s, %s);"
            cur.execute(sql,(uid,user_name, email, password,club_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # usersテーブルからメールアドレスを取得
    def getUser(email):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email=%s;"
            cur.execute(sql, (email))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # ログインユーザーのclub_idを取得
    def getUserClubId(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT club_id FROM users WHERE uid=%s;"
            cur.execute(sql, (uid))
            cid = cur.fetchone()
            user_club_id = cid['club_id']
            return user_club_id
        except Exception as e:
            print(str(e) + 'が発生しています１')
            abort(500)
        finally:
            cur.close()

    # ログインユーザーのclub_nameを取得
    def getUserClubName(user_club_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT club_name FROM clubs WHERE club_id=%s;"
            cur.execute(sql, (user_club_id))
            ucname = cur.fetchone()
            user_club_name = ucname['club_name']
            return user_club_name
        except Exception as e:
            print(str(e) + 'が発生しています２')
            abort(500)
        finally:
            cur.close()

    # ログインユーザーと同じclub_idを持つチャンネルを取得
    def getUserChannels(user_club_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE club_id=%s;"
            cur.execute(sql, (user_club_id))
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(str(e) + 'が発生しています３')
            abort(500)
        finally:
            cur.close()

    # ログインユーザーと同じclub_idを持つ新規チャンネルを追加
    def addChannel(uid, newChannelName, newChannelDescription, user_club_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (uid, name, abstract, club_id) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (uid, newChannelName, newChannelDescription, user_club_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # 入力されたチャンネル名と同じチャンネル名を取得
    # （ログインユーザーと同じclub_idのもののみ）
    def getChannelByName(channel_name,user_club_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE name=%s AND club_id=%s;"
            cur.execute(sql, (channel_name,user_club_id))
            channel = cur.fetchone()
        except Exception as e:
            print(e + 'が発生しました')
            abort(500)
        finally:
            cur.close()
            return channel

    # チャンネルIDを取得
    def getChannelById(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # チャンネル更新
    def updateChannel(uid, newChannelName, newChannelDescription, cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;"
            cur.execute(sql, (uid, newChannelName, newChannelDescription, cid))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しました')
            abort(500)
        finally:
            cur.close()

    # チャンネルを削除
    def deleteChannel(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


#DBから部活一覧を取得
    def getClubs():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM clubs ORDER BY club_id ASC;"
            cur.execute(sql)
            clubs = cur.fetchall()
            return clubs
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    def getMessageAll(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT id,u.uid, user_name, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #メッセージを挿入する
    def createMessage(uid,cid,message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor
            sql = "INSERT INTO messages (uid, cid, message) VALUES (%s, %s, %s);"
            cur.execute(sql,(uid,cid,message))
            conn.commit()
        except Exception as e:
            print(str(e)+'が発生しています')
            abort(500)
        finally:
            cur.close()

    #メッセージを削除する
    def deleteMessage(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM messages WHERE id=%S"
            cur.execute(sql,(message_id))
            conn.commit()
        except Exception as e:
            print(str(e)+'が発生しています')
            abort(500)
        finally:
            cur.close()

    def getChannelAll():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE club_id = {club_id};"
            cur.execute(sql)
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

