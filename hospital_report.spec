# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec 文件
- 入口脚本: main.py (项目根目录 GUI 程序)
- 主要目标: 在 Windows 下打包为单个应用目录（非单文件），包含 JSON 配置和模板等资源

在 Windows 上使用方法（在本项目根目录执行）:
  pyinstaller hospital_report.spec
"""

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # 配置文件
        ('config.json', '.'),

        # JSON 页面配置
        ('pages/*.json', 'pages'),

        # 报告模板及配置
        ('vest_database/templates/*', 'vest_database/templates'),

        # 旧版 arch 下可能仍被引用的字体/模板（以防脚本或 Excel 引用）
        ('arch/SIMSUN.ttf', '.'),
        ('arch/template/*', 'arch/template'),
    ],
    hiddenimports=[
        # tkcalendar / babel 相关，有时不会被自动发现
        'babel.numbers',
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
    [],
    exclude_binaries=True,
    name='hospital_report',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI 程序，不弹出控制台
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='hospital_report',
)


