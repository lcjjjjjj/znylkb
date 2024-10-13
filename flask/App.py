from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from Textsum import text_rewrite, text_translate, text_summarize
from Ifasr import file_asr
from Rtasr import rtasr_start, rtasr_stop
from fileconvert import f_convert
from filemanager import get_file_list, save_text_file
from usermanager import user_login, user_register, user_update
import os
import hashlib

app = Flask(__name__)
CORS(app, resources=r'/*')

process = None

@app.route("/")
def hello():
    return "<p>hello,world</p>"

@app.route('/upload', methods=['POST','GET'])
def recv_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        f = f.read()
        result = file_asr(f,filename)
        print(result)
        # f.save(f.filename)
        response = {
            'msg': result
        }
    return jsonify(response)

@app.route('/textsum', methods=['POST'])
def recv_text():
    data = request.json
    print(data)
    if data['task'] == 'first':
        result = text_rewrite(data['text'])
    elif data['task'] == 'second':
        result = text_translate(data['text'])
    elif data['task'] == 'save':
        result = save_text_file(data['text'], data['username'])
    else:
        result = text_summarize(data['text'])
    # print(result)
    response = {
        'msg': result
    }
    return jsonify(response)

@app.route('/textfileupload', methods=['POST'])
def recv_text_file():
    f = request.files['file']
    f = f.read()
    file_content = f.decode('utf-8')
    # print(f.decode('utf-8'))
    return jsonify({'msg': file_content})

@app.route('/rtasr', methods=['POST'])
def rt_asr():
    global process
    flag = request.json
    if flag['text'] == 'start':
        process = rtasr_start()
    else:
        rtasr_stop(process)
    return jsonify({'msg':'test'})

@app.route('/result', methods=['POST'])
def get_result():
    flag = request.json
    if flag['text'] == 'keep':
        with open('temp','r') as f:
            result = f.read()
            f.close()
    return jsonify({'msg': result})
    
@app.route('/clear', methods=['POST'])
def temp_clear():
    flag = request.json
    if flag['text'] == 'clear':
        with open('temp','w') as f:
            f.close()
        if os.path.exists('./audio_temp.wav'):
            os.remove('./audio_temp.wav')
    return jsonify({'msg':'200'})

@app.route('/download',methods=['GET'])
def download_audiofile():
    print(request.args.get)
    if request.args.get('file') == 'asrfile':
        if os.path.exists('audio_temp.wav'):
            return send_file('audio_temp.wav',as_attachment=True,download_name='audio_temp.wav')
        else:
            return jsonify({'msg': 'NotFound'})
    elif request.args.get('file') == 'wavfile':
        if os.path.exists('./temp_save.wav'):
            return send_file('temp_save.wav',as_attachment=True,download_name='temp_save.wav')
        else:
            return jsonify({'msg': 'NoFileUpload'})
    elif request.args.get('file') == 'mp3file':
        if os.path.exists('./temp_save.mp3'):
            return send_file('temp_save.mp3',as_attachment=True,download_name='temp_save.mp3')
        else:
            return jsonify({'msg': 'NoFileUpload'})
    elif request.args.get('file') == 'textfile':
        filename = request.args.get('filename')
        print(type(filename))
        username = request.args.get('username')
        cname = hashlib.sha256(username.encode('utf-8')).hexdigest()
        filepath = '/home/user/code/znylkb/flask/filecache/'+cname+'/'+filename
        return send_file(filepath,as_attachment=True,download_name=filename)
    else:
        return jsonify({'msg': 'NoFileUpload'})
    
@app.route('/convert',methods=['POST','GET'])
def convert_file():
    f = request.files['file']
    filetype = f.filename.split('.')[1]
    f_convert(f)
    return jsonify({'msg':'200 OK'})

@app.route('/delete',methods=['DELETE'])
def delete_file():
    if os.path.exists('temp_save.wav'):
        os.remove('temp_save.wav')
    elif os.path.exists('temp_save.mp3'):
        os.remove('temp_save.mp3')
    return jsonify({'msg': 'delete successfully'})

@app.route('/getfilelist', methods=['GET','POST'])
def send_list():
    # print(request.args.get('user'))
    user = request.args.get('user')
    return_data = get_file_list(user)
    return jsonify(return_data)

@app.route('/useroption', methods=['POST'])
def user_option():
    print(request.json)
    request_data = request.json
    if request_data['task'] == 'login':
        response = user_login(request_data['username'],request_data['password'])
        if response == True:
            return jsonify({'msg':'success'})
        else:
            return jsonify({'msg':'failed'})
    elif request_data['task'] == 'register':
        response = user_register(request_data['username'],request_data['password'])
        if response == True:
            return jsonify({'msg':'success'})
        elif response == False:
            return jsonify({'msg':'failed'})
        else:
            return jsonify({'msg':'error'})
        
@app.route('/userupdate', methods=['POST'])
def user_update_function():
    request_data = request.json
    response = user_update(request_data['username'],request_data['password'])
    if response == True:
        return jsonify({'msg':'success'})
    else:
        return jsonify({'msg':'failed'})

@app.route('/test', methods=['POST','GET'])
def request_test():
    return jsonify({'msg':'200 OK'})
