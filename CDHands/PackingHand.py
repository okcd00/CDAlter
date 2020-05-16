# -*- coding: gbk -*-
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
import PyInstaller.__main__


def packing(python_path='MainWindow.py'):
    name = 'Dummy App'
    # TODO: why `unable to load the file system codec`
    PyInstaller.__main__.run([
        '-F',
        # '--name={}'.format(name),  # set exe name
        # '--onedir',
        # '--nowindowed',
        '--icon=../CDNerve/res/cd_16x16.ico',
        '--debug=all',  # debug mode
        '--upx-dir=../resources/',
        r'--workpath=../data/tmp/',
        r'--distpath=../data/release/',
        '--hidden-import=threading',
        '--clean',
        # '--add-data={0};.'.format('redacted.xml'),
        # '--add-data={0};.'.format('redacted.pdf'),
        # '--exclude-module=../'.format('.git'),
        '--log-level=WARN',
        '{0}'.format(python_path)
    ])


if __name__ == '__main__':
    # packing('./bcr_time_counter.py')
    print(sys.version)
    print(sys.getdefaultencoding())
    packing('../examples/hello_world.py')

