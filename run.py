from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.utils import secure_filename
import os
import pandas as pd
from analyze_pcap import summary_data
from pretty_html_table import build_table
from tqdm import tqdm

# INSTANCES AND CONFIG #
app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'files'
app.config['ALLOWED_EXTENSIONS'] = ['.pcap', '.pcapng']
app.config['SECRET_KEY'] = 'syper_secret_key'
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
    return render_template('form.html', title='Проверить файл')

@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['ALLOWED_EXTENSIONS'] or file_ext != validate_file(uploaded_file.stream):
                flash(message='Неверный формат или битый файл', category='danger')
            else:
                uploaded_file.save(
                    os.path.join(app.config['UPLOAD_PATH'], 
                    filename
                    ))
                session['filename'] = filename
                flash('Загрузилось', category='success')
                return redirect(url_for('result'))
        else:
            flash('Выбери файл', category='danger')
    return redirect(url_for('result'))

@app.route('/result', methods=['GET'])
def result():
    filename = session.get('filename', None)
    file = os.path.join(app.config['UPLOAD_PATH'], filename)
    output = summary_data(file)
    if isinstance(output, str): #check if output of func is str
        return render_template('result.html', title='Результат', output=output)
    else: #output of func is tuple of dataframes
        dataframe_1, dataframe_2 = output
        dataframe_1_columns = list(dataframe_1.columns)
        dataframe_1_values = list(dataframe_1.values)
        dataframe_2_columns = list(dataframe_2.columns)
        dataframe_2_values = list(dataframe_2.values)
        return render_template('result.html', title='Результат', columns1=dataframe_1_columns, value1=dataframe_1_values, columns2=dataframe_2_columns, value2=dataframe_2_values)
# ROUTES #

# RUN #
if __name__ == "__main__":
    if 'files' not in os.listdir('.'):
        os.mkdir('files')
    app.run(debug=True)
# RUN #