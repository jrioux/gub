import os

from gub import mirrors
from gub import misc
from gub import repository
from gub import toolsbuild
from gub import cross

class Nsis (toolsbuild.SConsBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/nsis/nsis-2.37-src.tar.bz2'
    FOOsource = repository.CVS ('downloads/nsis',
                             source=':pserver:anonymous@nsis.cvs.sourceforge.net:/cvsroot/nsis',
                             module='NSIS',
                             tag='HEAD')
    def add_mingw_env (self):
        # Do not use 'root', 'usr', 'cross', rather use from settings,
        # that enables changing system root, prefix, etc.
        mingw_dir = (self.settings.alltargetdir + '/mingw'
                     + self.settings.root_dir)
        mingw_bin = (mingw_dir
                     + self.settings.prefix_dir
                     + self.settings.cross_dir
                     + '/bin')
        return {'PATH': mingw_bin + ':' + os.environ['PATH'] }
        
    def __init__ (self, settings, source):
        toolsbuild.AutoBuild.__init__ (self, settings, source)
# ugh, no object yet?
#  File "gub/cross.py", line 121, in setup_linux_x86
#    package.func (defer_compiler_checks)
#  File "gub/context.py", line 228, in func
#    return self.runner.func (f, *args)
#AttributeError: 'NoneType' object has no attribute 'func'
        if False and 'x86_64-linux' in self.settings.build_architecture:
            cross.setup_linux_x86 (self, self.add_mingw_env ())
        
    def get_build_dependencies (self):
        if 'x86_64-linux' in self.settings.build_architecture:
            return ['linux-x86::glibc']
        return []

    def patch (self):
        self.system ('mkdir -p %(allbuilddir)s', ignore_errors=True)
        self.system ('ln -s %(srcdir)s %(builddir)s')
        if self.settings.build_architecture.startswith ('x86_64-linux'):
            self.file_sub ([('''^Export\('defenv'\)''', '''
import os
defenv['CC'] = os.environ['CC']
defenv['CXX'] = os.environ['CXX']
Export('defenv')
''')],
                       '%(srcdir)s/SConstruct')
        
    def compile_command (self):
        return (toolsbuild.SConsBuild.compile_command (self)
                + misc.join_lines ('''
DEBUG=yes
NSIS_CONFIG_LOG=yes
SKIPUTILS="NSIS Menu"
SKIPPLUGINS=System
'''))

    # this method is overwritten for x86-64_linux
    def build_environment (self):
        return self.add_mingw_env ()
    
    def compile (self):
        if 'x86_64-linux' in self.settings.build_architecture:
            cross.setup_linux_x86 (self, self.add_mingw_env ())
        self.system ('cd %(builddir)s && %(compile_command)s',
                     self.build_environment ())

    def install (self):
        self.system ('cd %(builddir)s && %(install_command)s ',
                     self.build_environment ())

