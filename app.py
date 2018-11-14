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

def getData(a):
    db = sqlite3.connect("./directory.db")
    cur = db.cursor()
    cur.execute(a)
    db.commit()
    results = cur.fetchall()
    db.close()
    print(results)
    patient=results
    return results

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method =="POST":
        sql ='''INSERT INTO directory (OwnerLast, OwnerFirst, PetName, PetType, Notes) VALUES ('{}','{}','{}','{}','{}')'''.format(request.form["ownerLast"],request.form["ownerFirst"],request.form["petName"],request.form["petType"],request.form["note"])
#sql ='''INSERT INTO directory (OwnerLast, OwnerFirst, PetName, PetType, Notes) VALUES ("Carr","Betty","Blackberry","Cat","needs an appt")'''
        print(sql)
        sendSQL(sql)
#patientList = getData()
    return render_template("add.html")

@app.route('/manage', methods=['GET','POST'])
def manage():
    if request.method == "GET":

        lookup = '''SELECT * FROM directory WHERE PetName = "Maggie"'''
        getData(lookup)
        all='''SELECT * FROM directory'''
        directory=getData(all)

    return render_template("manage.html", directory=directory)


if __name__ == "__main__":
    app.run()
