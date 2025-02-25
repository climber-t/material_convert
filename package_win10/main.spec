# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
# 自动收集email子模块
from PyInstaller.utils.hooks import collect_submodules
a = Analysis(
    ['main.py'],
    pathex=['D:\\Pycharm_project\\material_new\\material_new\\material-main\\package_win10'],
    binaries=[],
    datas=[
        ('sort_number.py', '.'),
        ('generate_all.py', '.'),
        ('split_excel.py', '.'),
        ('concat.py', '.'),
        ('style.css', '.'),
        ('rocket.ico', '.')
    ],
    excludes=[
        'tkinter',
        'PyQt5.uic',
        'PyQt5.QtOpenGL',
        'PyQt5.QtPrintSupport',
        'PyQt5.QtQmlModels',
        'PyQt5.QtQml',
        'PyQt5.QtQuick',
        'PyQt5.QtQuickWidgets',
        'PyQt5.QtWebChannel',
        'PyQt5.QtWebSockets',
        'PyQt5.QtLocation',
        'PyQt5.QtPositioning',
        'PyQt5.QtBluetooth',
        'PyQt5.QtNfc',
        'PyQt5.QtMacExtras',
        'PyQt5.QtAndroidExtras',
        'PyQt5.QtWinExtras',
        'PyQt5.QtX11Extras',
        'PyQt5.QtMultimedia',
        'PyQt5.QtMultimediaWidgets',
        'PyQt5.QtV8Engine',
        'unittest',
        'test'
    ],
    hiddenimports=[
        'natsort',
        'pandas',
        'openpyxl',
        'pandas._libs.tslibs',
        'pandas._libs.tslibs.nattype',
        'xlrd',
        'split_excel',  # 显式包含自定义模块
        'sort_number', 
        'concat', 
        'generate_all', 
        'pandas._libs.tslibs.base',
    ] + collect_submodules('email'),  # 自动收集email子模块
    hookspath=['hooks'],  # 确保钩子目录正确
    hooksconfig={},
    runtime_hooks=[],
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
    name='MaterialApp',
    debug=False,
    onefile=True,  # 修正逗号
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='rocket.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)