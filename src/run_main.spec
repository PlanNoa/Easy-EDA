# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

hiddenimports=[
    "streamlit"
],

a = Analysis(
    ['run_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (
            "C:/Users/user/miniconda3/envs/streamQuality/Lib/site-packages/altair/vegalite/v4/schema/vega-lite-schema.json",
            "./altair/vegalite/v4/schema/"
        ),
        (
            "C:/Users/user/miniconda3/envs/streamQuality/Lib/site-packages/streamlit/static",
            "./streamlit/static"
        ),
        (
            "C:/Users/user/miniconda3/envs/streamQuality/Lib/site-packages/streamlit-1.19.0.dist-info",
            "./streamlit/streamlit-1.19.0.dist-info"
        ),
        (
            "C:/Users/user/PycharmProjects/cvtools/StreamQuality/main.py",
            "."
        ),
        (
            "C:/Users/user/miniconda3/envs/streamQuality/Lib/site-packages/numpy",
            "./numpy"
        )
    ],
    hiddenimports=[
        "streamlit", "pandas", "numpy", "matplotlib", "openpyxl", "xlrd", "time", "streamlit.runtime.scriptrunner.magic_funcs"
    ],
    hookspath=['./hooks'],
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
    name='run_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
