# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Explicitly specify the hidden imports (modules that weren't auto-detected)
hiddenimports = [
    'mysql.connector.plugins.caching_sha2_password',
    'mysql.connector.locales.eng'
]

a = Analysis(['main.py'],
             pathex=['/Users/aj/Desktop/SalesSystem'],
             binaries=[],
             datas=[
                 ('database/config.toml', 'database'),
                 ('resources/icons/*', 'resources/icons'),
                 ('resources/images/*', 'resources/images'),
                 ('resources/styles.css', 'resources')
             ],
             hiddenimports=hiddenimports,  # Include the hidden imports
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,  # Set to False for GUI applications
          icon='resources/icons/logo.icns')  # Specify the icon path
