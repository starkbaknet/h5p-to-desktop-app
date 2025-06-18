import os
import shutil
import zipfile
import subprocess
import json
from flask import Flask, request, render_template, send_file
import requests

UPLOAD_FOLDER = 'uploads'
BUILD_FOLDER = 'builds'
GENERATED_FOLDER = 'generated'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BUILD_FOLDER'] = BUILD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BUILD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

CONVERT_API = 'http://localhost:8080/convert'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        h5p_file = request.files['h5p_file']
        project_name = request.form['project_name']

        if h5p_file and project_name:
            file_path = os.path.join(UPLOAD_FOLDER, h5p_file.filename)
            h5p_file.save(file_path)

            # Step 1: Convert H5P to SCORM
            with open(file_path, 'rb') as f:
                response = requests.post(CONVERT_API, files={
                    'h5p_file': f,
                    'h5p_mastery_score': (None, '80')
                })

            if response.status_code != 200:
                return f"API Conversion failed: {response.status_code}"

            # Step 2: Save and unzip SCORM
            zip_path = os.path.join(BUILD_FOLDER, f'{project_name}_scorm.zip')
            with open(zip_path, 'wb') as f:
                f.write(response.content)

            unzip_folder = os.path.join(BUILD_FOLDER, f'{project_name}_unzipped')
            os.makedirs(unzip_folder, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_folder)

            # Step 3: Create Neutralino project
            neutralino_path = os.path.join(BUILD_FOLDER, project_name)
            subprocess.run(['neu', 'create', project_name], cwd=BUILD_FOLDER, check=True)

            # Step 4: Patch config for window closing
            config_path = os.path.join(neutralino_path, 'neutralino.config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r+') as f:
                    config = json.load(f)
                    config.setdefault("window", {})["enableNativeWindowExit"] = True
                    config.setdefault("modes", {}).setdefault("window", {})["exitProcessOnClose"] = True
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()

            # Step 5: Copy SCORM content into resources
            resources_path = os.path.join(neutralino_path, 'resources')
            for item in os.listdir(unzip_folder):
                src = os.path.join(unzip_folder, item)
                dst = os.path.join(resources_path, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

            # Step 6: Build the app
            subprocess.run(['neu', 'build'], cwd=neutralino_path, check=True)

            # Step 7: Package app (DMG or EXE)
            script_path = os.path.abspath(os.path.join('scripts', 'build_desktop.py'))
            subprocess.run(['python3', script_path, project_name, neutralino_path], check=True)

            # Step 8: Find the generated installer
            generated_file = None
            for root, dirs, files in os.walk(neutralino_path):
                for file in files:
                    if file.endswith('.dmg') or file.endswith('.exe'):
                        generated_file = os.path.join(root, file)
                        break
                if generated_file:
                    break

            if not generated_file:
                return render_template('index.html', download_link=None)

            # Step 9: Move to 'generated/' folder
            final_dest = os.path.join(GENERATED_FOLDER, os.path.basename(generated_file))
            shutil.move(generated_file, final_dest)

            # Step 10: Clean only contents (not folders)
            for folder in [UPLOAD_FOLDER, BUILD_FOLDER]:
                for item in os.listdir(folder):
                    path = os.path.join(folder, item)
                    try:
                        if os.path.isfile(path) or os.path.islink(path):
                            os.unlink(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                    except Exception as e:
                        print(f'Failed to delete {path}. Reason: {e}')

            # Step 11: Return download link to template
            final_filename = os.path.basename(final_dest)
            return render_template(
                'index.html',
                download_link=f"/download/{final_filename}",
                file_name=final_filename
            )

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(GENERATED_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run()
