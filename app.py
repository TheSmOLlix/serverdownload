from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

# Folder, w którym będą zapisywane pliki
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Strona główna z formularzem do wprowadzenia URL
@app.route('/')
def index():
    return render_template('index.html')

# Obsługuje pobieranie filmu
@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    
    # Opcje pobierania
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, 'video.%(ext)s'),  # Zmieniamy nazwę na "video"
        'noplaylist': True,
    }

    try:
        # Pobieranie filmu
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = 'video.' + info_dict['ext']  # Stosujemy nazwę 'video' z odpowiednim rozszerzeniem
            
            # Zwrócenie pliku do przeglądarki
            return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
