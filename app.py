from flask import Flask, redirect, url_for, render_template, session, request, jsonify
import db_operator as myDB

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



# restAPI section

@app.route('/API/tasklist', methods=['GET'])
def APItasklist():
    username = session.get('username', '')
    if username == '':
        username = 'default'
        session['username']=username
    tasks = myDB.showTasks(username)
    if tasks == None:
        return render_template("loginerror.html")
    tasks = [{'id':task[0], 'todo':task[1], 'urgent':task[2]} for task in tasks]
    return jsonify(tasks)

@app.route('/API/tasklist', methods=['POST'])
def APIaddTask():
    username = session.get('username', '')
    if username == '':
        username = 'default'
        session['username']=username
    newTask = request.json
    ret = myDB.newTask(newTask['todo'], username)
    return jsonify([{'todo':ret}])

@app.route('/API/tasklist/<TaskID>', methods=['GET'])
def APIgetTaskContent(TaskID):
    username = session.get('username', '')
    if username == '':
        username = 'default'
        session['username'] = username
    task = myDB.getTaskContent(TaskID)
    if task=='':
        return jsonify([{'id':'', 'todo':'', 'urgent':''}])
    task = [{'id':task[0], 'todo':task[1], 'urgent':task[2]}]
    return jsonify(task)

@app.route('/API/tasklist/<id>/update', methods=['POST'])
def APIupdateTaskByID(id):
    username = session.get('username', '')
    if username == '':
        username = 'default'
        session['username']=username
    updatedTask = request.json
    TaskID = updatedTask.get('id', '')
    todo = updatedTask.get('todo', '')
    urgent = updatedTask.get('urgent', '')
    ret = myDB.updateTask(TaskID, todo, urgent)
    if ret > 0:
        return jsonify([{'id': TaskID, 'todo': todo, 'urgent': urgent}])
    return jsonify([{'id':'', 'todo':'', 'urgent':''}])

@app.route('/API/tasklist/<id>', methods=['DELETE'])
def APIdeleteTaskByID(id):
    username = session.get('username', '')
    if username == '':
        username = 'default'
        session['username']=username
    ret = myDB.removeTask(id, username)
    if ret > 0:
        return jsonify([{'id': id, 'deleted':'true'}])
    return jsonify([{'id':'', 'deleted':'false'}])


if __name__ == '__main__':
    app.run()
