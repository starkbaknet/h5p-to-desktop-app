import sys
import os
import subprocess
import platform
import shutil

project_name = sys.argv[1]
project_path = sys.argv[2]

# Neutralino build output path
build_dir = os.path.join(project_path, 'dist', project_name)
os.makedirs(build_dir, exist_ok=True)

output_file = None

if platform.system() == 'Darwin':
    app_name = project_name
    dmg_script = os.path.abspath('scripts/create_dmg.sh')

    # Binary path
    built_binary = os.path.join(build_dir, f"{project_name}-mac_universal")
    if not os.path.isfile(built_binary):
        raise FileNotFoundError(f"Expected binary not found: {built_binary}")

    # App bundle paths
    app_bundle = os.path.join(project_path, f'{app_name}.app')
    contents_dir = os.path.join(app_bundle, 'Contents')
    macos_dir = os.path.join(contents_dir, 'MacOS')
    resources_dir = os.path.join(contents_dir, 'Resources')

    # Clean any old .app
    if os.path.exists(app_bundle):
        shutil.rmtree(app_bundle)

    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)  # Temporarily, can be deleted later

    # ✅ Copy only the binary
    binary_dest = os.path.join(macos_dir, project_name)
    shutil.copy2(built_binary, binary_dest)
    os.chmod(binary_dest, 0o755)

    # ✅ Copy only resources.neu (no platform files)
    resources_neu_path = os.path.join(build_dir, 'resources.neu')
    if os.path.exists(resources_neu_path):
        shutil.copy2(resources_neu_path, os.path.join(macos_dir, 'resources.neu'))

    # ✅ Create minimal Info.plist
    plist_path = os.path.join(contents_dir, 'Info.plist')
    with open(plist_path, 'w') as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleExecutable</key>
    <string>{project_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.{project_name.lower()}</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
""")

    # ✅ Optionally remove now-empty Resources dir
    if os.path.exists(resources_dir):
        shutil.rmtree(resources_dir)

    # ✅ Build DMG
    env = os.environ.copy()
    env['APP_NAME'] = app_name
    subprocess.run(['bash', dmg_script], cwd=project_path, check=True, env=env)

    output_file = os.path.join(project_path, f'{app_name} Installer.dmg')

elif platform.system() == 'Windows':
    nsis_template = os.path.abspath('scripts/create_installer.nsi')
    output_file = os.path.join(build_dir, f'{project_name}_installer.exe')

    with open(nsis_template, 'r') as f:
        nsis_content = f.read().replace('{{APP_NAME}}', project_name).replace('{{OUTPUT_FILE}}', output_file)

    nsis_script = os.path.join(project_path, 'installer_temp.nsi')
    with open(nsis_script, 'w') as f:
        f.write(nsis_content)

    subprocess.run(['makensis', nsis_script], cwd=project_path, check=True)

else:
    print("Unsupported platform.")
    sys.exit(1)

# ✅ Final output used by Flask
with open(os.path.join(project_path, 'final_output_path.txt'), 'w') as f:
    f.write(output_file)
