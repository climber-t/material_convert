# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(
    ['main.py'],
    pathex=['D:\\Pycharm_project\\material_new\\material_new\\material-main\\package_win7'],
    binaries=[],
    datas=[
        ('sort_number.py', '.'),
        ('generate_all.py', '.'),
        ('split_excel.py', '.'),
        ('concat.py', '.'),
        ('style.css', '.'),
        ('rocket.ico', '.')
    ],
    hiddenimports=[
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'openpyxl.styles.stylesheet'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 保留核心排除项
        'PyQt5.QtWebEngine*', 
        'PyQt5.QtNetwork',
        'PyQt5.QtSql',
        'PyQt5.Qt3D*',
        'pandas.plotting',
        'pandas.io.html',
        'unittest',
        'email'
    ],
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
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='rocket.ico',
    disable_windowed_traceback=False
)