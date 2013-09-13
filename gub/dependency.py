import new
import os
#
from gub.syntax import printf
from gub import cross
from gub import gub_log
from gub import misc
from gub import repository
from gub import system
from gub import target
from gub import tools
from gub import tools32

def get_build_from_file (platform, file_name, name):
    gub_name = file_name.replace (os.getcwd () + '/', '')
    gub_log.verbose ('reading spec: %(gub_name)s\n' % locals ())
    # Ugh, FIXME
    # This loads gub/specs/darwin/python.py in PYTHON. namespace,
    # overwriting the PYTHON. namespace from gub/specs/python.py
    # Current workaround: always/also use __darwin etc. postfixing
    # of class names, also in specs/darwin/ etc.
    module = misc.load_module (file_name, name)
    # cross/gcc.py:Gcc will be called: cross/Gcc.py,
    # to distinguish from specs/gcc.py:Gcc.py
    base = os.path.basename (name)
    class_name = ((base[0].upper () + base[1:])
                  .replace ('-', '_')
                  .replace ('.', '_')
                  .replace ('++', '_xx_')
                  .replace ('+', '_x_')
                  + ('-' + platform).replace ('-', '__'))
    gub_log.debug ('LOOKING FOR: %(class_name)s\n' % locals ())
    cls = misc.most_significant_in_dict (module.__dict__, class_name, '__')
    if (platform == 'tools32'
        and (not cls or issubclass (cls, target.AutoBuild))):
        cls = misc.most_significant_in_dict (module.__dict__, class_name.replace ('tools32', 'tools'), '__')
    if ((platform == 'tools' or platform == 'tools32')
        and (not cls or issubclass (cls, target.AutoBuild)
             and not issubclass (cls, tools.AutoBuild)
             and not issubclass (cls, tools32.AutoBuild))):
        cls = None
    return cls

def get_build_class (settings, flavour, name):
    cls = get_build_from_module (settings, name)
    if not cls:
        gub_log.verbose ('making spec:  %(name)s\n' % locals ())
        cls = get_build_without_module (flavour, name)
    if cls:
        cls._created_name = name
    return cls

def get_build_from_module (settings, name):
    file = get_build_module (settings, name)
    if file:
        cls = get_build_from_file (settings.platform, file, name)
        if not cls and settings.platform == settings.build_platform:
            cls = get_build_from_file ('tools', file, name)
        return cls
    return None

def get_build_module (settings, name):
    file_base = name + '.py'
    for dir in (os.path.join (settings.specdir, settings.platform),
                os.path.join (settings.specdir, settings.os),
                settings.specdir):
        file_name = os.path.join (dir, file_base)
        if os.path.exists (file_name):
            return file_name
    return None

def get_build_without_module (flavour, name):
    '''Direct dependency build feature

    * gub http://ftp.gnu.org/pub/gnu/tar/tar-1.18.tar.gz
    WIP:
    * gub git://git.kernel.org/pub/scm/git/git
    * bzr:http://bazaar.launchpad.net/~yaffut/yaffut/yaffut.bzr
    * must remove specs/git.py for now to get this to work
    * git.py overrides repository and branch settings'''
    
    cls = new.classobj (name, (flavour,), {})
    cls.__module__ = name
    return cls

class Dependency:
    def __init__ (self, settings, name, url=None):
        # FIXME: document what is accepted here, and what not.
        if not name and not url:
            raise Exception ('''Dependency without name or url: check for empty string in dependency list: ['']''')

        self.settings = settings
        self._name = name

        if misc.is_ball (name):
            self._name = misc.name_from_url (name)
            
        self._cls = self._flavour = None
        self._url = url

    def _create_build (self):
        dir = os.path.join (self.settings.downloads, self.name ())
        branch = self.settings.__dict__.get ('%(_name)s_branch' % self.__dict__,
                                             self.build_class ().branch)
        source = self.url ()
        if not isinstance (source, repository.Repository):
            source = repository.get_repository_proxy (dir, source, branch)
        gub_log.default_logger.write_log ('cls:' + str (self.build_class ()) + '\n', 'output')
        return self.build_class () (self.settings, source)

    def build_class (self):
        if not self._cls:
            self._cls = get_build_class (self.settings, self.flavour (),
                                         self.name ())
        return self._cls

    def flavour (self):
        if not self._flavour:
            self._flavour = target.AutoBuild
            if self.settings.platform == 'system':
                self._flavour = system.Configure
            elif self.settings.platform == 'tools':
                self._flavour = tools.AutoBuild
            elif self.settings.platform == 'tools32':
                self._flavour = tools32.AutoBuild
        return self._flavour
    
    def url (self):
        if not self._url:
            self._url = self.build_class ().source
        if not self._url:
            gub_log.warning ('no source specified in class: '
                             + self.build_class ().__name__ + '\n')
        if not self._url:
            self._url = self.settings.dependency_url (self.name ())
        if not self._url:
            raise Exception ('No URL for: '
                             + misc.with_platform (self._name,
                                                   self.settings.platform))
        if type (self._url) == str:
            try:
                self._url = self._url % self.settings.__dict__
            except:
                printf ('URL:', self._url)
                raise
            x, parameters = misc.dissect_url (self._url)
            if parameters.get ('patch'):
                self._cls.patches = parameters['patch']
            if parameters.get ('dependency'):
                self._cls.build_dependencies = parameters['dependency']
        return self._url
    def name (self):
        return self._name
    def build (self):
        b = self._create_build ()
        cross.get_cross_module (self.settings).change_target_package (b)
        b.source.settings = self.settings
        return b
