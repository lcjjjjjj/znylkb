# -*- encoding:utf-8 -*-
import hashlib
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging
import pyaudio
import multiprocessing
import signal
import wave
import os

# reload(sys)
# sys.setdefaultencoding("utf8")
class Client():
    def __init__(self,appId,apiKey):
        self.api_key = apiKey
        self.app_id = appId
        base_url = "ws://rtasr.xfyun.cn/v1/ws"
        ts = str(int(time.time()))
        tt = (self.app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = self.api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        self.end_tag = "{\"end\": true}"

        self.ws = create_connection(base_url + "?appid=" + self.app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()


    def rt_send(self, chunk_size=1024, sample_rate=16000, channels=1):
        # 初始化PyAudio并打开音频流
        p = pyaudio.PyAudio()
        with wave.open('audio_temp.wav','wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            stream = p.open(format=pyaudio.paInt16, channels=channels,
                            rate=sample_rate, input=True, frames_per_buffer=chunk_size)
            # 开始音频流
            stream.start_stream()
            try:
                while True:
                    # 从麦克风读取音频数据
                    audio_data = stream.read(chunk_size)
                    # 保存音频临时文件
                    wf.writeframes(audio_data)
                    # 发送到服务器
                    self.ws.send(audio_data)

                    # 可以在这里添加逻辑来决定何时停止发送，例如检测静音或达到特定时间

            except KeyboardInterrupt:
                # 用户中断时的处理
                pass
            finally:
                # 停止音频流并关闭资源
                stream.stop_stream()
                stream.close()
                p.terminate()
                wf.close()

            # 发送结束标签
            self.ws.send(bytes(self.end_tag.encode('utf-8')))
            print("send end tag success")

    def recv(self):
        try:
            text_final = ''
            text_temp = ''
            while self.ws.connected:
                text = ''
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    break
                result_dict = json.loads(result)
                # 解析结果
                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)

                if result_dict["action"] == "result":
                    data = json.loads(result_dict['data'])
                    # print("rtasr result: " + result_1["data"])
                    sentence = data['cn']['st']['rt']
                    # print(result)
                    for index in range(len(sentence)):
                        word_set = sentence[index]['ws']
                        # print(word_set)
                        for item in word_set:
                            text += item['cw'][0]['w']
                    if len(text_temp) <= len(text):
                        text_temp = text
                    elif len(text_temp) > len(text) and not(text in text_temp):
                        text_final += text_temp
                        text_temp = ''
                    # print(text_final+text)
                    with open('temp','w') as f:
                        f.write(text_final+text)
                        f.close()

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
            # print(text_final)
        except websocket.WebSocketConnectionClosedException:
            text = ''
            text_final = ''
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")


def rtasr_start():
    logging.basicConfig()

    app_id = "bdc8a74f"
    api_key = "af8b855977814f4c4b3718255f24dea3"

    client = Client(app_id,api_key)
    process = multiprocessing.Process(target=client.rt_send)
    process.start()
    return process
    
    
def rtasr_stop(process):
    os.kill(process.pid,signal.SIGINT)
    process.join()