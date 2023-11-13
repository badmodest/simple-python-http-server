import os
import sys
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = '2kd8shcD1#@*&$!Qhc02k4ne17'


def get_directory_contents(path):
    items = os.listdir(path)
    files = []
    folders = []

    for item in items:
        item_path = os.path.join(path, item)
        last_modified = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%Y-%m-%d %H:%M:%S')
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            files.append((item, last_modified, size))
        else:
            folders.append((item, last_modified))

    return folders, files

@app.route('/')
def list_directory():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    folders, files = get_directory_contents(current_directory)
    return render_template('index.html', folders=folders, files=files, path="", active_folder=current_directory)

@app.route('/directory/<path:subpath>')
def list_subdirectory(subpath):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.join(current_directory, subpath)
    folders, files = get_directory_contents(directory_path)
    return render_template('index.html', folders=folders, files=files, path=subpath, active_folder=current_directory)

@app.route('/download/<path:filename>')
def download_file(filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, filename)
    return send_from_directory(current_directory, filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), uploaded_file.filename)
            uploaded_file.save(file_path)
    return redirect(url_for('list_directory'))

@app.route('/index')
def index():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    folders, files = get_directory_contents(current_directory)
    return render_template('index.html', folders=folders, files=files, path="", active_folder=current_directory)

users = {
    'user1': 'password1',
    'user2': 'password2',
}

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    render_template('auth.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['username'] = username  
            flash('Вы успешно вошли', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильный логин или пароль', 'error')

    return render_template('auth.html')

if __name__ == '__main__':
    ip_address = '127.0.0.1'
    port = 5000
    silent = False

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == '--ip':
            ip_address = sys.argv[i + 1]
        elif sys.argv[i] == '--port':
            port = int(sys.argv[i + 1])
        elif sys.argv[i] == '--silent':
            silent = True
        elif sys.argv[i] == '--auth':
            app.run(host=ip_address, port=port, use_reloader=False)
            sys.exit()

    if not silent:
        app.run(host=ip_address, port=port)
    else:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        app.run(host=ip_address, port=port, use_reloader=False)
