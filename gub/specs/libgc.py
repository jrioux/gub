from gub import target

class Libgc (target.AutoBuild):
    configure_flags = target.AutoBuild.configure_flags + ' --enable-threads=pthreads'
    #source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-7.1.tar.gz'
    source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc6.8.tar.gz&version=6.8'

class Libgc__freebsd (Libgc):
    make_flags = 'THREADDLLIBS=-pthread'
    patches = ['libgc_6.8-1.2ubuntu2.diff']

class Libgc__freebsd__x86 (Libgc__freebsd):
    source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc6.8.tar.gz&version=6.8'
    #patches = ['libgc-6.8-freebsd-x86_64.patch']

class Libgc__mingw (Libgc):
    dependencies = [
        'pthreads-w32',
        ]
    patches = [
        'libgc-6.8-mingw-pthreads.patch',
        ]
    force_autoupdate = True
    source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc6.8.tar.gz&version=6.8'
