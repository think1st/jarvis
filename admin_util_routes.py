# Add to your web_admin.py
from flask import send_file
import subprocess
import shutil

@app.route('/download-backup')
def download_backup():
    subprocess.run(['bash', 'backup.sh'])
    backup_folder = "backup"
    newest = sorted(os.listdir(backup_folder))[-1]
    return send_file(os.path.join(backup_folder, newest), as_attachment=True)

@app.route('/upload-backup', methods=['POST'])
def upload_backup():
    file = request.files['backup_zip']
    path = os.path.join("backup", "uploaded.zip")
    os.makedirs("backup", exist_ok=True)
    file.save(path)
    shutil.unpack_archive(path, '.')
    return redirect(url_for('index'))

@app.route('/check-updates', methods=['POST'])
def check_updates():
    subprocess.run(['bash', 'update.sh'])
    return redirect(url_for('index'))
