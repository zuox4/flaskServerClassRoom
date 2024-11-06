import random

from flask import Flask, request, render_template, jsonify
import os

from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import send_file
import os
from flask import redirect
import datetime

import pars_dialary

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def upload_form():
    images = os.listdir(UPLOAD_FOLDER)
    images = [os.path.join(UPLOAD_FOLDER, image) for image in images if allowed_file(image)]
    return render_template('upload.html', images=images)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Проверка наличия файла в запросе
    if 'file' not in request.files:
        return 'Нет выбранного файла', 400
    file = request.files['file']
    # Если файл пустой, возвращаем ошибку
    if file.filename == '':
        return 'Нет выбранного файла', 400
    # Если файл допустимый, сохраняем его в папку
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')


# URL для доступа к загруженным изображениям

@app.route('/get_images/<url>')
def get_image(url):
    directory = "uploads"
    files = os.listdir(directory)
    filename = f'uploads/{url}'
    return send_file(filename, mimetype='image/gif')

#Галерея класса
@app.route('/get_routs_imgs')
def get_routs_imgs():
    directory = "uploads"
    files = os.listdir(directory)
    list = [f'http://127.0.0.1:5000/get_images/{i}' for i in files]
    return jsonify({'photos': list})

#Расписание класса
@app.route('/get_dailary')
def get_dailary_today():
    try:
        date = datetime.datetime.now().date()
        data = pars_dialary.get_dialary(date)
        return jsonify({'data':data})
    except:
        return jsonify({'data':[]}), 404




if __name__ == "__main__":
    app.run(debug=True)
