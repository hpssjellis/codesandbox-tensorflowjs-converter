# tfjs-to-keras-flask03.py



from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import tensorflowjs as tfjs
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './myUp'  # Update this path    # MUST MAKE THESE FOLDERS
# Update this path
app.config['CONVERTED_MODEL_FOLDER'] = './myConverted'
# Path for the zipped file
app.config['MODEL_ZIP_PATH'] = './myZipped'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'json', 'bin'}


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def convert_tfjs_to_keras(tfjs_model_path, keras_model_output_path):
    try:
        model = tfjs.converters.load_keras_model(tfjs_model_path)
        model.save(keras_model_output_path)
        print(f"Model converted and saved to {keras_model_output_path}")

        zipf = zipfile.ZipFile(
            app.config['MODEL_ZIP_PATH'], 'w', zipfile.ZIP_DEFLATED)
        zipdir(keras_model_output_path, zipf)
        zipf.close()
        print("Model zipped successfully")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return 'No files part in the request'

        files = request.files.getlist('files[]')
        if not files:
            return 'No files selected'

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        tfjs_model_path = os.path.join(
            app.config['UPLOAD_FOLDER'], files[0].filename)
        convert_tfjs_to_keras(
            tfjs_model_path, app.config['CONVERTED_MODEL_FOLDER'])

        return redirect(url_for('download_model'))

    return '''
    <!doctype html>
    <title>Upload multiple files</title>
    <h1>Upload TensorFlow.js Model and Weights</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=files[] multiple>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/download_model')
def download_model():
    try:
        return send_file(app.config['MODEL_ZIP_PATH'], as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
