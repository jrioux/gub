from gub import target

class Xulrunner (target.AutoBuild):
    source = 'http://ftp.mozilla.org/pub/mozilla.org/xulrunner/releases/1.9.0.3/source/xulrunner-1.9.0.3-source.tar.bz2'
    config_cache_flag_broken = True

class Xulrunner__mingw (Xulrunner):
    def patch (self):
        self.file_sub ([('#! /bin/sh', '#! /bin/bash\nenable -n pwd')],
                       '%(srcdir)s/configure')
    dependencies = ['mingw-pwd']
