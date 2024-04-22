
import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests


def download_file_from_url(url, destination):
    response = requests.get(url)
    with open(destination, "wb") as f:
        f.write(response.content)

app = Flask(__name__)

# Load the trained model
model_url = 'https://drive.google.com/uc?export=download&id=1TdpLpCIFY4m0vS7eIlETj6occA6CbZWg'

destination_path = 'model.h5'

download_file_from_url(model_url, destination_path)

model = load_model('model.h5')


# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            return redirect(url_for('predict', filename=filename))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

# Route for predicting
@app.route('/predict/<filename>')
def predict(filename):
    img = image.load_img(os.path.join('uploads', filename), target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    result = 'Asian Hornet' if prediction[0][0] > 0.5 else 'Other Insect'
    return render_template('result.html', filename=filename, result=result)

if __name__ == '__main__':
    app.run(debug=True)
