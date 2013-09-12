from gub import tools

class Neon__tools (tools.AutoBuild):
    source = 'http://www.webdav.org/neon/neon-0.28.4.tar.gz'
    dependencies = [
            'expat',
            'openssl',
            'zlib',
            ]
    configure_flags = tools.AutoBuild.configure_flags \
                    + ' --with-ssl'
