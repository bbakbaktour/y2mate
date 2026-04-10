from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import glob

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    try:
        # 기존 파일 삭제 (중복 방지)
        for f in glob.glob("downloaded*"):
            os.remove(f)

        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # ffmpeg 없이 mp4 우선
            'outtmpl': 'downloaded.%(ext)s',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 파일 찾기
        files = glob.glob("downloaded*")
        if not files:
            return "다운로드 실패 (파일 없음)"

        return send_file(files[0], as_attachment=True)

    except Exception as e:
        return f"에러 발생: {str(e)}"


# Render용 실행
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
