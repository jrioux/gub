from gub import target

class Lash (target.AutoBuild):
    source = 'http://download.savannah.gnu.org/releases/lash/lash-0.6.0~rc2.tar.bz2'
    patches = ['lash-0.6.0.rc2.patch']
    dependencies = ['tools::automake', 'tools::pkg-config',
                'e2fsprogs-devel',
                'dbus-devel',
                'jack-devel',
                ]
    configure_flags = (target.AutoBuild.configure_flags
                + '--without-python')
        # either that, or
        # + 'CPPFLAGS="-I%(system_prefix)s/include `python-config --cflags`"'
        # + 'LDFLAGS="`python-config --ldflags`"')
