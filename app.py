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
    sql = '''SELECT * FROM directory'''
    cur.execute(sql)
    results = cur.fetchall()
    db.close()
    return results

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method =="POST":
        sql ='''INSERT INTO directory (OwnerLast, OwnerFirst, PetName, PetType, Notes) VALUES "{}','{}','{}','{}','{}"'''.format(request.form["ownerLast"],request.form["ownerFirst"],request.form["petName"],request.form["petType"],request.form["note"])
        #sql ='''INSERT INTO directory (OwnerLast, OwnerFirst, PetName, PetType, Notes) VALUES ("Carr","Betty","Blackberry","Cat","needs an appt")'''
        print(sql)
        sendSQL(sql)
    directory = getData()
    return render_template("add.html", directory=directory)

@app.route('/manage', methods=['GET','POST'])
def manage():
    if request.method == "GET":
        db = sqlite3.connect("./directory.db")
        cur = db.cursor()
        #lookup = '''SELECT * FROM directory WHERE PetName ="{}"'''.format(request.form["petName"]
        lookup = '''SELECT * FROM directory WHERE PetName ="Maggie"'''
        cur.execute(lookup)
        db.commit()
        results = cur.fetchall()
        db.close()
        filterDirectory=results
        return render_template("manage.html", directory=filterDirectory)
    elif request.method == "POST":
        db = sqlite3.connect("./directory.db")
        cur = db.cursor()
        note = request.form['update']
        print (note)
        if note=="Delete":
            update='''DELETE FROM directory WHERE ID="{}"'''.format(request.form[petID])
        elif note != "Delete":
            update = '''UPDATE directory SET Notes = "{}".format(request.form["update"] WHERE ID="{}".format(request.form[petID])'''
        cur.execute(update)
        db.commit()
        results = getData()
        db.close()
        print(results)
        updatedDirectory = results
        return render_template("manage.html", directory=updatedDirectory)

if __name__ == "__main__":
    app.run()