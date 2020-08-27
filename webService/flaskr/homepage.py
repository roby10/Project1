import os
import numpy as np
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model2 = load_model('../../saved_model/')
labels = ['backview', 'car_features', 'engine', 'frontview', \
        'interior', 'sideview', 'trunk']

height, width = 512, 290

app = Flask(__name__)
dropzone = Dropzone(app)

app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.jpg'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
app.config['SECRET_KEY'] = '1337Testing'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if "file_urls" not in session:
        session['file_urls'] = []

    file_urls = session['file_urls']

    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)

            filename = photos.save(
                file,
                name=file.filename    
            )

            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
    return render_template('homepage.html')

@app.route('/results')
def results():
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('homepage'))
        
    file_urls = session['file_urls']
    session.pop('file_urls', None)

    imgs = []

    for file in file_urls:
        file = file.split('/')[-1]
        img = img_to_array(load_img(app.config['UPLOADED_PHOTOS_DEST'] + '/' +  file, target_size=(height, width)))/255.0
        imgs.append(img)

    imgs = np.array(imgs)

    dict = {}

    res = model2.predict(imgs)

    res = np.argmax(res, axis=1)

    for label in labels:
        dict[label] = []

    for idx in range(len(res)):
        dict[labels[res[idx]]].append(file_urls[idx])

    return render_template('results.html', dict=dict)