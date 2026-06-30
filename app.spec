# app.spec
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

a = Analysis(
    ['WebApp.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('templates', 'templates'),          # HTML templates + static files
    ],
    hiddenimports=[
        'waitress',
        'waitress.runner',
        'werkzeug',
        'werkzeug.security',
        'werkzeug.serving',
        'flask',
        'jinja2',
        'jinja2.ext',
        'click',
        'itsdangerous',
        'email',
        'email.mime',
        'email.mime.text',
        'email.mime.multipart',
        'smtplib',
        'ssl',
        'sqlite3',
        'hashlib',
        'secrets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubeClone',           # <- Your app's .exe name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                      # Compress the exe (smaller size)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                 # False = no black CMD window pops up
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
icon='templates/static/Icons/youtube.ico',
)