# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['market8591.py'],
             pathex=['F:\\marketworkspace\\mk85_Program'],
             binaries=[],
             datas=[],
             hiddenimports=['pagespidy', 'getproxy', 'setting', 'proxypool', 'proxypool01', 'proxypool02','changeproxy','detail_gui'],
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
          [
          ('\\src\\db\\proxy_List.csv','F:\\marketworkspace\\mk85_Program\\src\\db\\proxy_List.csv','DATA'),
          ('\\src\\image\\bg.png','F:\\marketworkspace\\mk85_Program\\src\\image\\bg.png','DATA'),
          ('\\src\\image\\bg01.png','F:\\marketworkspace\\mk85_Program\\src\\image\\bg01.png','DATA'),
          ('\\src\\image\\icon.jpg','F:\\marketworkspace\\mk85_Program\\src\\image\\icon.jpg','DATA'),
          ('\\src\\image\\icon_ana.png','F:\\marketworkspace\\mk85_Program\\src\\image\\icon_ana.png','DATA'),
          ('\\src\\image\\icon_prx.png','F:\\marketworkspace\\mk85_Program\\src\\image\\icon_prx.png','DATA'),
          ('\\src\\image\\image.png','F:\\marketworkspace\\mk85_Program\\src\\image\\image.png','DATA'),
          ('\\src\\image\\noimage.png','F:\\marketworkspace\\mk85_Program\\src\\image\\noimage.png','DATA'),
          ('\\src\\webdriver\\chromedriver.exe','F:\\marketworkspace\\mk85_Program\\src\\webdriver\\chromedriver.exe','DATA'),
          ],
          name='market8591',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
