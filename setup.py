#!/usr/bin/env python

from distutils.core import setup
import glob, os

def pluginsFolders():
    basepath = "pyazan/plugins"
    for dir in os.listdir(basepath):
        plugin = os.path.join(basepath, dir)
        if os.path.isdir(plugin):
            yield plugin

print list(pluginsFolders())
setup(name='PyAzan',
      version='0.1',
      description='Python Azan Notifier',
      author='Jo De Boeck',
      author_email='deboeck.jo@gmail.com',
      url='http://github.com/grimpy/pyazan',
      packages=['pyazan', 'pyazan/plugins'] + list(pluginsFolders()),
      scripts=['pyazangtk'],
      data_files=[('share/pixmaps/pyazan', glob.glob('data/*.png')),
                  ('share/pixmaps/', ['data/pyazan_icon.png']),
                  ('share/sounds/pyazan', ['data/azan.mp3']),
                  ('share/applications', ['data/PyAzan.desktop']),
                  ('share/icons/hicolor/16x16/apps', glob.glob('data/icons/16x16/apps/*.png')),
                  ('share/icons/hicolor/22x22/apps', glob.glob('data/icons/22x22/apps/*.png')),
                  ('share/icons/hicolor/24x24/apps', glob.glob('data/icons/24x24/apps/*.png')),
                  ('share/icons/hicolor/32x32/apps', glob.glob('data/icons/32x32/apps/*.png')),
                  ('share/icons/hicolor/48x48/apps', glob.glob('data/icons/48x48/apps/*.png')),
                  ('share/pyazan/ui/', glob.glob('ui/*.xml'))]
     )
