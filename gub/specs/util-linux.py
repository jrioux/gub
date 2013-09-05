#
from gub import tools

class Util_linux__tools (tools.AutoBuild):
    source = 'http://www.kernel.org/pub/linux/utils/util-linux/v2.16/util-linux-ng-2.16.tar.gz'
    dependencies = ['libtool']
    configure_flags = (tools.AutoBuild.configure_flags
                + ' --disable-tls'
                + ' --disable-makeinstall-chown'
                + ' SHELL=%(tools_prefix)s/bin/bash'
                + ''' CFLAGS='-DLINE_MAX=1024' ''')
