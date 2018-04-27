
import db_operator as myDB
from flask import Flask, redirect, url_for, render_template, session, request

import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

app = Flask(__name__)
app.secret_key = "veryveryveryfucsdakjkkingseckjsbtydfdcretkey"



@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    username = session.get('username', '')
    if username != '':
        return redirect(url_for('taskList'))
    else:
        return render_template("index.html")

@app.route('/tasklist', methods=['POST'])
def taskList():
    username = session.get('username', '')
    if username=='':
        username = request.form['username']
        session['username'] = username
    tasks = myDB.showTasks(username)
    return render_template("tasklist.html", tasks=tasks, username=username)

@app.route('/tasklist', methods=['GET'])
def taskListGet():
    username = session.get('username', '')
    tasks = myDB.showTasks(username)
    print(tasks)
    return render_template("tasklist.html", tasks=tasks, username=username)

@app.route('/deletetask', methods=["POST"])
def deleteTask():
    username = session.get('username', '')
    if(username==''):
        print("errore, nome non esistente")
    else:
        task_id = request.form['task_id']
        res = myDB.removeTask(task_id, username)
        if res==0:
            print("non ho cancellato un cazzo?")
        else:
            print("ho cancellato il task con id: " + task_id + " appartenente ad: " + username)
    return redirect(url_for('index'))

@app.route('/addtask', methods=["POST"])
def addTask():
    username = session.get('username', '')
    if(username==''):
        print("errore, nome non esistente")
    else:
        todo = request.form['todo']
        res = myDB.newTask(todo, username)
        if res==0:
            print("non ho inserito un cazzo?")
        else:
            print("ho inserito il task con id: " + todo + " appartenente ad: " + username)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    del (session['username'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
