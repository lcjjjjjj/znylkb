import pymysql
import hashlib
from filemanager import create_user_dir

db = pymysql.connect(host='localhost',
                     user='root',
                     passwd='11235813',
                     database='znylkb')

cursor = db.cursor()

def user_login(username, password):
    cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
    record = cursor.fetchone()
    if record == None:
        return False
    else:
        if record[2] == password:
            return True
        else:
            return False
        
def user_register(username, password):
    cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
    record = cursor.fetchone()
    cid = hashlib.sha256((username).encode('utf-8')).hexdigest()
    if record != None:
        return False
    elif record == None:
        try:
            sql = f"INSERT INTO `users`(`username`,`cpassword`,`cid`) VALUES('{username}','{password}','{cid}');"
            cursor.execute(sql)
            db.commit()
            create_user_dir(cid)
            return True
        except:
            db.rollback()
            return 'Error'
    return 'Error'
    

def user_update(username, password):
    sql = f"UPDATE `users` SET `cpassword`='{password}' WHERE `username`='{username}'"
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except:
        db.rollback()
        return False
    return False
        