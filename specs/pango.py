import glob
import os
import shutil
import download
import misc
import targetpackage
import re

class Pango (targetpackage.TargetBuildSpec):
    def __init__ (self, settings):
        targetpackage.TargetBuildSpec.__init__ (self, settings)
        self.with (version='1.12.3',
                   mirror=download.gnome_214,
                   format='bz2')

    def get_build_dependencies (self):
        return ['freetype-devel', 'fontconfig-devel', 'glib-devel',
                'libtool']

    def get_dependency_dict (self):
        return {'': ['freetype', 'fontconfig', 'glib', 'libtool-runtime']}

    def configure_command (self):
        return targetpackage.TargetBuildSpec.configure_command (self) \
           + misc.join_lines ('''
--without-x
--without-cairo
''')

    def configure (self):
        targetpackage.TargetBuildSpec.configure (self)                
        self.update_libtool ()
    def patch (self):
        targetpackage.TargetBuildSpec.patch (self)
        self.system ('cd %(srcdir)s && patch --force -p1 < %(patchdir)s/pango-substitute-env.patch')

    def fix_modules (self):
        etc = self.expand ('%(install_root)s/usr/etc/pango')
        self.system ('mkdir -p %(etc)s' , locals ())
        for a in glob.glob (etc + '/*'):
            self.file_sub ([('/usr/', '$PANGO_PREFIX/')],
                   a)

        pango_module_version = None
        for dir in glob.glob (self.expand ("%(install_prefix)s/lib/pango/*")):
            m = re.search ("([0-9.]+)", dir)
            if not m:
                continue
            
            pango_module_version = m.group (1)
            break
        
        if not pango_module_version:
            raise 'No version found'
        
        open (etc + '/pangorc', 'w').write (
        '''[Pango]
ModuleFiles = $PANGO_PREFIX/etc/pango/pango.modules
ModulesPath = $PANGO_PREFIX/lib/pango/%(pango_module_version)s/modules
''' % locals ())
        
        shutil.copy2 (self.expand ('%(sourcefiledir)s/pango.modules'),
               etc)


    def install (self):
        targetpackage.TargetBuildSpec.install (self)                
        self.dump ("""
setfile PANGO_RC_FILE=$INSTALLER_PREFIX/etc/pango/pangorc
setdir PANGO_PREFIX=$INSTALLER_PREFIX/
""", '%(install_root)s/usr/etc/relocate/pango.reloc', env=locals())

        self.fix_modules ()

class Pango__linux (Pango):
    def untar (self):
        Pango.untar (self)
        # FIXME: --without-cairo switch is removed in 1.10.1,
        # pango only compiles without cairo if cairo is not
        # installed linkably on the build system.  UGH.
        self.file_sub ([('(have_cairo[_a-z0-9]*)=true', '\\1=false'),
                        ('(cairo[_a-z0-9]*)=yes', '\\1=no')],
                       '%(srcdir)s/configure')
        os.chmod ('%(srcdir)s/configure' % self.get_substitution_dict (), 0755)

## placeholder, don't want plain Pango for freebsd.
## Pango 1.12 broken FreeBSD? It tries to load NCSB for Chinese glyphs.

class Pango__freebsd (Pango__linux):
    def __init__ (self, settings):
        Pango__linux.__init__ (self, settings)
        self.with (version='1.11.2',
             mirror=download.gnome_213,
             format='bz2')

    def get_build_dependencies (self):
        return Pango__linux.get_build_dependencies (self) + ['libiconv-devel']

    def install (self):
        Pango__linux.install (self)
        for f in ['%(install_root)s/usr/etc/pango/pangorc',
                  '%(install_root)s/usr/etc/pango/pango.modules']:
            self.file_sub ([('pango/1.5.0/', 'pango/1.4.0/')], f)
            

class Pango__darwin (Pango):
    def configure (self):
        Pango.configure (self)
        self.file_sub ([('nmedit', '%(target_architecture)s-nmedit')],
                       '%(builddir)s/libtool')

    def install (self):
        Pango.install (self)                
        self.dump ("""
set PANGO_SO_EXTENSION=.so
""", '%(install_root)s/usr/etc/relocate/pango.reloc', env=locals(), mode="a")
