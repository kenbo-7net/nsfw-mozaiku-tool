from flask import Flask, request, send_file, render_template_string
import os
import shutil
from nsfw_mosaic import process_images

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HTML_FORM = '''
<!doctype html>
<title>NSFWモザイクツール</title>
<h1>画像アップロード</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=アップロードして処理>
</form>
{% if filename %}
  <p>処理完了: <a href="{{ url_for('download_file', filename=filename) }}">{{ filename }}</a></p>
{% endif %}
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
        shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            process_images(input_dir=UPLOAD_FOLDER, output_dir=OUTPUT_FOLDER)
            return render_template_string(HTML_FORM, filename=filename)

    return render_template_string(HTML_FORM)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
