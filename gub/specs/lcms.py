from gub import target

class Lcms (target.AutoBuild):
    source = 'http://downloads.sourceforge.net/project/lcms/lcms/1.17/lcms-1.17.tar.gz'
    dependencies = ['tools::libtool']
    def configure (self):
        target.AutoBuild.configure (self)
        self.system ('rm -f %(srcdir)s/include/icc34.h')
