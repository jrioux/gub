from gub import tools

class Alien (tools.CpanBuild):
    source = 'https://launchpad.net/ubuntu/+archive/primary/+files/alien_8.60.tar.gz'
    srcdir_build_broken = True
    def srcdir (self):
        return '%(allsrcdir)s/alien'
    def configure (self):
        tools.CpanBuild.configure (self)
        self.system ('cd %(srcdir)s && patch -p0 < %(patchdir)s/alien.patch')

