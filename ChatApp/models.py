import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
    def createUser(user):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql="INSERT INTO users (uid,name, email, password,club) VALUES (%s,%s,%s,%s,%s,%s);"
            cur.execute(sql,(user.uid.user.user_name, user.email, user.password,user.club_id))
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

    def getClubId(club_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT club_id FROM clubs WHERE club_name=%s;"
            cur.execute(sql, (club_name,))
            clubid = cur.fetchone()
            return clubid
        except Exception as e:
            print(str(e) + 'が発生しています')
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

#チャンネルの削除
def deleteChannel(cid):
    try:
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "DELETE FROM channels WHERE id=%s;"
        cur.execute(sql,(cid))
        conn.commit()
    except Exception as e:
        print(e + 'が発生しています')
        return None
    finally:
        cur.close()
