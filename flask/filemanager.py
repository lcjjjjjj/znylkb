import os
import time
import hashlib

def get_file_list(user):
    cache_path = '/home/user/code/znylkb/flask/filecache'
    user_dirname = hashlib.sha256(user.encode('utf-8')).hexdigest()
    user_path = os.path.join(cache_path,user_dirname)
    print(user_path)
    filelist = os.listdir(user_path)
    return_data = []
    for f in filelist:
        ctime = os.stat(os.path.join(user_path,f)).st_ctime
        create_time = time.ctime(ctime)
        print(create_time)
        filesize = os.path.getsize(os.path.join(user_path,f))
        filetype = f.split('.')[-1]
        return_data.append({
            'date': create_time,
            'name': f,
            'size': str(filesize),
            'tag': filetype
        })
    return return_data

def create_user_dir(dir_name):
    cache_path = '/home/user/code/znylkb/flask/filecache'
    os.mkdir(os.path.join(cache_path,dir_name))


def save_text_file(text, username):
    cache_path = '/home/user/code/znylkb/flask/filecache'
    user_dir = hashlib.sha256(username.encode('utf-8')).hexdigest()
    save_path = os.path.join(cache_path,user_dir)
    filename = hashlib.md5((username+str(len(os.listdir(save_path)))).encode('utf-8')).hexdigest()+'.txt'
    with open(os.path.join(save_path,filename),'w') as f:
        f.write(text)
    f.close()
    return 'Done'