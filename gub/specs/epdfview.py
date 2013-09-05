from gub import target

class Epdfview (target.AutoBuild):
    source = 'https://launchpad.net/ubuntu/+archive/primary/+files/epdfview_0.1.7.orig.tar.gz'
    dependencies = [
            'tools::automake',
            'tools::gettext',
            'tools::libtool',
            'tools::pkg-config',
            'gtk+-devel',
            'lilypondcairo',
            'poppler-devel',
            ]
    configure_flags = (target.AutoBuild.configure_flags
                       + ' --without-cups'
                       )

class Epdfview__mingw (Epdfview):
    patches = ['epdfview-0.1.7-mingw.patch']
