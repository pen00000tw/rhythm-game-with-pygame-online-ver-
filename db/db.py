# db.py
import mysql.connector

con = mysql.connector.connect(
    host="www.kuanmin.tk",
    user="root",
    passwd="vm6ej04aup6",
    database="game"
)

cursor = con.cursor()

#make a function to access the db
def user_login(tup):
    try:
        cursor.execute("SELECT * FROM player WHERE user_id=%s AND password=%s",tup)
        return (cursor.fetchone())
    except:
        return False
def user_check(tup):
    try:
        SQL = "SELECT * FROM player WHERE user_id=%s"
        cursor.execute(SQL,(tup,))
        return (cursor.fetchone())
    except mysql.connector.Error as err:
        return False
def user_register(tup):
    try:
        SQL = "INSERT INTO player(user_id,user_name,password) VALUES(%s,%s,%s)"
        cursor.execute(SQL,tup)
        con.commit()
    except mysql.connector.Error as err:
        return False
def rank(tup):
    try:
        SQL = "select * FROM record WHERE songname=%s ORDER BY score DESC"
        cursor.execute(SQL,(tup,))
        return (cursor.fetchall())
    except mysql.connector.Error as err:
        return False
def record(tup):
    try:
        SQL = "select * FROM record WHERE name=%s ORDER BY date DESC"
        cursor.execute(SQL,(tup,))
        return (cursor.fetchall())
    except mysql.connector.Error as err:
        return False
def writerecord(tup):
    try:
        print(tup)
        SQL = "INSERT INTO record(name,score,songname) VALUES(%s,%s,%s)"
        cursor.execute(SQL,tup)
        con.commit()
    except mysql.connector.Error as err:
        print(err)
        return False

