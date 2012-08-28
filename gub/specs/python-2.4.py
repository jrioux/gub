from gub import target
from gub import tools
from gub.specs import python

def get_conflict_dict (self):
    return {
        '': ['python-2.6', 'python'],
        'doc': ['python-2.6-doc', 'python-doc'],
        'devel': ['python-2.6-devel', 'python-devel'],
        'runtime': ['python-2.6-runtime', 'python-runtime'],
        }

class Python_2_4 (python.Python):
    get_conflict_dict = get_conflict_dict
class Python_2_4__mingw (python.Python__mingw):
    get_conflict_dict = get_conflict_dict
class Python_2_4__mingw_binary (python.Python__mingw_binary):
    get_conflict_dict = get_conflict_dict
class Python_2_4__freebsd (python.Python__freebsd):
    get_conflict_dict = get_conflict_dict
class Python_2_4__tools (python.Python__tools):
    get_conflict_dict = get_conflict_dict
