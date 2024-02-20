import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
    def createUser(uid, user_name, email, password,club_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql="INSERT INTO users (uid,user_name, email, password,club_id) VALUES (%s,%s,%s,%s,%s);"
            cur.execute(sql,(uid,user_name, email, password,club_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

#DBから部活をとってくる
    def getClubsAll():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM clubs ORDER BY club_id ASC;"
            cur.execute(sql)
            clubs = cur.fetchall()
            print(clubs)
            return clubs
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()
