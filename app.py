from flask import Flask, request, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': 'downloaded.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith("downloaded") and file.endswith(".mp4"):
            return send_file(file, as_attachment=True)

# --- 이 아랫부분이 수정되었습니다 ---
if __name__ == '__main__':
    # Render는 PORT 환경 변수를 통해 포트를 지정해줍니다.
    # host를 '0.0.0.0'으로 설정해야 외부 접속이 가능합니다.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
