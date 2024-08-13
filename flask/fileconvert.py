from pydub import AudioSegment
import io

def f_convert(file):
    filename = file.filename
    f = file.read()
    print(type(f))
    filetype = filename.split('.')[1]
    if filetype == 'wav':
        wav_io = io.BytesIO(f)
        audio = AudioSegment.from_wav(wav_io)
        mp3_io = io.BytesIO()
        audio.export(mp3_io,format="mp3")
        mp3_data = mp3_io.getvalue()
        with open('temp_save.mp3',"wb") as file:
            file.write(mp3_data)
            file.close()
    else:
        mp3_io = io.BytesIO(f)
        audio = AudioSegment.from_mp3(mp3_io)
        wav_io = io.BytesIO()
        audio.export(wav_io,format="wav")
        wav_data = wav_io.getvalue()
        with open('temp_save.wav',"wb") as file:
            file.write(wav_data)
            file.close()
