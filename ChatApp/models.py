import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
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

    # ログインしたユーザーのclub_idを取得
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

    # ログインしたユーザーのclub_nameを取得
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

    # ログインしたユーザーと同じclub_idを持つチャンネルを取得
    def getUserChannels(user_club_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE club_id=%s;"
            cur.execute(sql, (user_club_id))
            channels = cur.fetchone()
            return channels
        except Exception as e:
            print(str(e) + 'が発生しています３')
            abort(500)
        finally:
            cur.close()

#DBから部活をとってくる
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

    def getChannelAll():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels;"
            cur.execute(sql)
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

