from gub import target

class Libsndfile (target.AutoBuild):
    source = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.23.tar.gz'
    dependencies = [
        'tools::automake',
        'tools::pkg-config',
        'libtool',
        'sqlite'
        ]

class Libsndfile__darwin__x86 (Libsndfile):
    dependencies = [x for x in Libsndfile.dependencies
                if x.replace ('-devel', '') not in [
                'sqlite', # Included in darwin-x86 SDK, hmm?
                ]]
