from gub import target

class Kbproto (target.AutoBuild):
    source = 'http://xorg.freedesktop.org/releases/X11R7.4/src/everything/kbproto-1.0.3.tar.gz'
    dependencies = ['tools::libtool']
