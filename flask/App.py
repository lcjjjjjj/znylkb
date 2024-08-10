from flask import Flask, request, jsonify
from flask_cors import CORS
from Textsum import text_rewrite
from Ifasr import file_asr
from Rtasr import rtasr_start, rtasr_stop

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
    return jsonify({'msg':'200'})