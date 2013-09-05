from gub import target

class Jack (target.WafBuild):
    source = 'http://jackaudio.org/downloads/jack-1.9.9.5.tar.bz2'
    # requires python 2.6
    dependencies = ['tools::automake', 'tools::pkg-config',]
