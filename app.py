from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # アップロードされたファイルを保存するフォルダ

# ファイルを安全にアップロードするための設定
ALLOWED_EXTENSIONS = {'wav', 'mp3'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')  # HTMLファイルをレンダリング

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        flash('ファイルがありません')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('ファイルが選択されていません')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            with open(file_path, "rb") as audio_file:
                response = openai.Audio.transcribe("whisper-1", audio_file)
                transcript = response["text"]
        except Exception as e:
            print(f"An error occurred: {e}")
            return str(e)  # ここでエラー内容をクライアントに返す
        
        return render_template('index.html', transcription=transcript)
if __name__ == '__main__':
    app.run(debug=True)


#以下はAPIキーを環境変数
#echo "export OPENAI_API_KEY='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'" >> ~/.bashrc