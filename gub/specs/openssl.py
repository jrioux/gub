from gub import build

class OpenSSL__tools (build.AutoBuild):
    source = 'http://www.openssl.org/source/openssl-0.9.8y.tar.gz'
    dependencies = [
            'perl',
            ]
    # The configure script is named config
    configure_binary = '%(autodir)s/config'
    # Out-of-tree builds are not supported
    configure_command = 'cp -r %(autodir)s/* %(builddir)s && ' \
                    + build.AutoBuild.configure_command
    configure_flags = build.AutoBuild.configure_flags \
                    + ' --install-prefix=%(install_root)s'

Openssl__tools = OpenSSL__tools
