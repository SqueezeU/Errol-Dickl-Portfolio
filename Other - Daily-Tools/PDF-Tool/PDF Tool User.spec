# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['PDF_Tool_Devs.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Diese Liste verhindert, dass Anaconda seinen Ballast mit einpackt
    excludes=['pandas', 'matplotlib', 'sklearn', 'spacy', 'nltk', 'numpy', 'PyQt5', 'IPython', 'jupyter', 'PIL', 'sqlalchemy', 'scipy', 'bokeh', 'astropy', 'xarray'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PDF Tool User',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)