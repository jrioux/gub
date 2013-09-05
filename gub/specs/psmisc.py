from gub import target

class Psmisc (target.AutoBuild):
    source = 'http://downloads.sourceforge.net/project/psmisc/psmisc/Archive/psmisc-22.7.tar.gz'
    subpackage_names = ['']
    dependencies = ['ncurses']
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
ac_cv_func_malloc_0_nonnull=yes
ac_cv_func_realloc_0_nonnull=yes
'''
