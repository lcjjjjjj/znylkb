from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from Textsum import text_rewrite
from Ifasr import file_asr
from Rtasr import rtasr_start, rtasr_stop
from fileconvert import f_convert
import os

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
    result = text_rewrite(data['text'])
    # print(result)
    response = {
        'msg': result
    }
    return jsonify(response)

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

@app.route('/test', methods=['POST','GET'])
def request_test():
    return jsonify({'msg':'200 OK'})
