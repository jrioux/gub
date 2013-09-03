from gub.specs.cross import gcc as cross_gcc
from gub import misc

class Gcc__freebsd (cross_gcc.Gcc):
    source = 'http://ftp.gnu.org/pub/gnu/gcc/gcc-4.3.2/gcc-4.3.2.tar.bz2'
    dependencies = cross_gcc.Gcc.dependencies + ['tools::mpfr']
    configure_command = (''' LDFLAGS='-L%(tools_prefix)s/lib %(rpath)s' '''
                         + cross_gcc.Gcc.configure_command)
    configure_flags = (cross_gcc.Gcc.configure_flags
                + misc.join_lines ('''
--program-prefix=%(toolchain_prefix)s
'''))
    configure_variables = (cross_gcc.Gcc.configure_variables 
                + misc.join_lines ('''
MAKEINFO=no
'''))
