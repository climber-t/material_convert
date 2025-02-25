from PyInstaller.utils.hooks import collect_submodules, collect_data_files
hiddenimports = collect_submodules('PyQt5')
datas = collect_data_files('PyQt5', include_py_files=True)