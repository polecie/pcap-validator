from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename
import os
import imghdr

# INSTANCES AND CONFIG #
app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'files'
app.config['ALLOWED_EXTENSIONS'] = ['.pcap', '.pcapng']
app.config['SECRET_KEY'] = 'dsgsgsd'
# INSTANCE AND CONFIG #

# CHECK EXT #
def validate_file(stream):
    header = stream.read(32) #getting first 32 (pcap, pcapng) bytes of a file
    stream.seek(0)
    if b'\xd4\xc3\xb2\xa1' in header:
        format = 'pcap'
        return '.' + format
    if b'\x00M<+' in header:
        format = 'pcapng'
        return '.' + format
# CHECK EXT #

# ROUTES #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['ALLOWED_EXTENSIONS'] or file_ext != validate_file(uploaded_file.stream):
                flash(message='Проверь формат', category='danger')
            else:
                uploaded_file.save(
                    os.path.join(app.config['UPLOAD_PATH'], 
                    filename
                    ))
                flash(message='Загрузилось', category='success')

    return redirect(url_for('index'))
# ROUTES #

# RUN #
if __name__ == "__main__":
    app.run(debug=True)
# RUN #