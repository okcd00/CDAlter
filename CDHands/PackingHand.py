# -*- coding: utf-8 -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : PackingHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-05-16
#   desc     : Packing a program into an executable file.
#   require  : pyinstaller, upx
# ==========================================================================
import sys
sys.path.append('../')

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# os.environ['TCL_LIBRARY'] =
# os.environ['TK_LIBRARY'] =


def packing_with_pi(python_path='MainWindow.py'):
    import PyInstaller.__main__
    name = 'Dummy App'
    # TODO: why `unable to load the file system codec`
    PyInstaller.__main__.run([
        '-F',
        # '--name={}'.format(name),  # set exe name
        '--onedir',
        # '--nowindowed',
        '--noupx',
        # '--upx-dir=../resources/',
        '--icon=../CDNerve/res/cd_16x16.ico',
        '--debug=all',  # debug mode
        '--log-level=DEBUG',
        r'--workpath=../data/tmp/',
        r'--distpath=../data/release/',
        '--hidden-import=wx',
        '--clean',
        # '--add-data={0};.'.format('redacted.xml'),
        # '--add-data={0};.'.format('redacted.pdf'),
        # '--exclude-module=../'.format('.git'),
        '{0}'.format(python_path)
    ])


def packing_with_cx(python_path='MainWindow.py'):
    from cx_Freeze import setup, Executable
    # python PackingHand.py build/bdist_msi
    name = 'hello_world'
    options = {
        'build_exe': {
            "includes": ["CDNerve.BaseFrame"],
            'packages': ['os', 'wx'],
            # 'excludes': ['gtk', 'PyQt4', 'PyQt5', 'Tkinter'],
            "include_files": ["../CDNerve/res/cd_16x16.ico"],
            "path": sys.path,
        },
    }
    setup(name=name,
          version="0.0.1",
          description="",
          options=options,
          author="CDPlayer",
          executables=[
              Executable(
                  script=python_path,
                  base=base,
                  icon="../CDNerve/res/cd_16x16.ico",
              )
          ])


def packing(python_path):
    # return packing_with_pi(python_path)
    return packing_with_cx(python_path)


# packing('./bcr_time_counter.py')
print(sys.version)
sys.stdout = open('../data/tmp/packing.log', 'w')
packing('../examples/kari_crackme.py')

