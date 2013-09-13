from gub import tools

class Texinfo__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/pub/gnu/texinfo/texinfo-4.13a.tar.gz'
    patches = ['texinfo-4.13-dash.patch']
    def patch (self):
        tools.AutoBuild.patch (self)
        # Drop ncurses dependency
        self.file_sub ([(' info ',' ')], '%(srcdir)s/Makefile.in')
