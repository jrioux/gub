from gub import tools

class Docbook_utils__tools (tools.AutoBuild):
    source = 'ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES/docbook-utils-0.6.14.tar.gz'
    def get_build_dependencies (self):
        return ['jade']
