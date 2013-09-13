import os
import sys
#
from gub import misc
from gub import target
from gub.specs import inkscape

# FIXME: make target.Installer/target.BaseBuild packag?
# This is much more work than just calling
#   bin/gib --platform= --branch=PACKAGE=BRANCH PACKAGE
# not really a 'python driver'.
class Inkscape_installer (target.AutoBuild):
    source = inkscape.Inkscape.source
    never_install = 'True'
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        source.is_tracking = misc.bind_method (lambda x: True, source)
        source.is_downloaded = misc.bind_method (lambda x: True, source)
        source.update_workdir = misc.bind_method (lambda x: True, source)
        self.dependencies = [settings.target_platform + '::inkscape']
    subpackage_names = ['']
    def stages (self):
        return ['compile', 'install', 'package']
    def compile (self):
        inkscape_branch = self.source.full_branch_name ()
        self.system (sys.executable
                     + misc.join_lines ('''
bin/gib
--platform=%(target_platform)s
--branch=inkscape=%(inkscape_branch)s
inkscape
'''), locals ())
    install_command = 'true'
