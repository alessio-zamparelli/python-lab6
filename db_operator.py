import pymysql as sql
import configparser
import sys

config = configparser.ConfigParser()
config.read('config.ini')
confUser = config['mysql']['user']
confPwd = config['mysql']['password']
confDB = config['mysql']['database']
confHost = config['mysql']['host']



def start():
    con = sql.connect(user=confUser, password=confPwd, database=confDB, host=confHost)
    try:

        # print("db correttamente aperto")
        # update.message.reply_text("your user id is: " + str(update.message.from_user.id))
        cur = con.cursor()
        cur.execute(
            "create table if not exists 'task' (id integer primary key autoincrement, user_id integer ,todo varchar[255] not null)")
        con.commit()
        cur.close()
        con.close()
    except sql.DataError as DataErr:
        print("errore di creazione table " + DataErr.args[0])
    except sql.DatabaseError as DBerror:
        print("errore nell'apertura del db " + DBerror.args[0])
        sys.exit(1)

def showTasks(username):
    con = sql.connect(user=confUser, password=confPwd, database=confDB, host=confHost)
    try:
        cur = con.cursor()
        sql_query = "select id, todo, urgent from task where username = %s order by todo asc;"
        cur.execute(sql_query, (username,))
        rows = cur.fetchall()
        cur.close()
        con.close()
    except sql.DataError as DataErr:
        print("errore di creazione table " + DataErr.args[0])
    except sql.DatabaseError as DBerror:
        print("errore nell'apertura del db " + DBerror.args[0])
        sys.exit(1)

    if len(rows) == 0:
        return None
    #rows = [i[0] for i in rows]
    return rows

def getTaskContent(id):
    con = sql.connect(user=confUser, password=confPwd, database=confDB, host=confHost)
    try:
        cur = con.cursor()
        sql_query = "select id, todo, urgent from task where id = %s;"
        cur.execute(sql_query, (id,))
        row = cur.fetchone()
        cur.close()
        con.close()
    except sql.DataError as DataErr:
        print("errore di creazione table " + DataErr.args[0])
    except sql.DatabaseError as DBerror:
        print("errore nell'apertura del db " + DBerror.args[0])
        sys.exit(1)

    if row == None:
        return ""
    # rows = [i[0] for i in rows]
    return row

def newTask(todo, username):
    # msg = ' '.join(arg)
    if (todo != ""):
        con = sql.connect(user=confUser, password=confPwd, database=confDB, host=confHost)
        cur = con.cursor()
        sql_query = "insert into task (todo, username) values (%s, %s)"
        cur.execute(sql_query, (todo, username))
        con.commit()
        cur.close()
        con.close()

        # showTasks(bot, update)
        print("added " + todo + " to the tasks list")
        return todo
    else:
        print("empty task...")
        return ""

def updateTask(TaskID, todo, urgent):
    if (todo != ""):
        con = sql.connect(user=confUser, password=confPwd, database=confDB, host=confHost)
        cur = con.cursor()
        sql_query = "UPDATE task SET todo = %s, urgent = %s WHERE id = %s"
        ret = cur.execute(sql_query, (todo, urgent, TaskID))
        con.commit()
        cur.close()
        con.close()
        return ret

    else:
        print("empty task...")
        return [{'id':'', 'todo':'', 'urgent':''}]


def removeTask(task_id, username):
    # msg = ' '.join(args)
    try:
        con = sql.connect(user=confUser, password=confPwd, database=confDB, host=confHost)
        cur = con.cursor()
        sql_query = "delete from task where id = %s AND username=%s;"
        res = cur.execute(sql_query, (task_id, username))
        con.commit()
        cur.close()
        con.close()
        return res
    except ValueError:
        print("element not found!")



def removeAllTasks(arg):
    con = sql.connect(user=confUser, password=confPwd, database=confDB, host=confHost)
    cur = con.cursor()
    arg = '%' + arg + '%'
    cur.execute("delete from task where todo like %s ", (arg, ))
    con.commit()
    cur.close()
    con.close()
    print("Deleted ALL tasks containing " + arg)

if __name__ == '__main__':

    print(showTasks("ale"))
    #removeAllTasks("task")
    #task2 = "task di prova 2"
    #newTask(task2)
    #print(showTasks())
    #ret = showTasks()
    #tasks = [i[0] for i in ret]

    #print(tasks)
