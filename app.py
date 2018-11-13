import sqlite3, psycopg2
from flask import Flask, render_template, request

ps_endpoint = "valsvethospital.cq6v5mrlsvrf.us-east-2.rds.amazonaws.com"

sql = '''CREATE TABLE IF NOT EXISTS directory (id INTEGER PRIMARY KEY, OwnerLast TEXT, OwnerFirst TEXT, PetName TEXT, PetType TEXT, Notes TEXT)'''

def sendSQL(sql):
    db = sqlite3.connect("./directory.db")
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    db.close()

sendSQL(sql)

def getData():
    db = sqlite3.connect("./directory.db")
    cur = db.cursor()
    sql = 'SELECT * FROM directory'
    cur.execute(sql)
    db.commit()
    results = cur.fetchall()
    db.close()
    return results


app = Flask(__name__)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method =="POST":
        sql ='''INSERT INTO directory (OwnerLast, OwnerFirst, PetName, PetType, Notes) VALUES ('{}','{}','{}','{}','{}')'''.format(request.form["ownerLast"],request.form["ownerFirst"],request.form["petName"],request.form["petType"],request.form["note"])
        print(sql)
        sendSQL(sql)
    patientList = getData()
    return render_template("add.html", patientList=patientList)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/manage', methods=['GET','POST'])
def directory():
    directory = getData()
    return render_template("manage.html",directory=directory)

if __name__ == '__main__':
    app.run()
