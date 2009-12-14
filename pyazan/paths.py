import sys, os
def getFullPath(value):
    basepath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basepath, value)
def getPrefix():
    app = sys.argv[0]
    return os.path.dirname(os.path.dirname(app))

PREFIX=getPrefix()
PIXMAPS=SOUND=XML=None
if PREFIX.startswith("/usr"):
    SOUND = os.path.join(PREFIX, 'share', 'sounds', 'pyazan')
    XML = os.path.join(PREFIX, 'share', 'pyazan', 'ui')
    PIXMAPS = os.path.join(PREFIX, 'share', 'pixmaps', 'pyazan')
    TRAYICON=PIXMAPS+"_icon.png"
else:
    SOUND=PIXMAPS=getFullPath("../data")
    XML=getFullPath("../ui/")
    TRAYICON=os.path.join(PIXMAPS, "pyazan_icon.png")

XDG_HOME = os.environ.get("XDG_CONFIG_HOME")
if not XDG_HOME:
    XDG_HOME = os.path.expanduser(os.path.join("~", ".config"))
CONFIGPATH = os.path.join(XDG_HOME, "pyazan.cfg")
ICON = os.path.join(PIXMAPS, "pyazan.png")
