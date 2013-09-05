from gub import target

class Base_passwd (target.AutoBuild):
    source = 'https://launchpad.net/ubuntu/+archive/primary/+files/base-passwd_3.5.11.tar.gz'
    srcdir_build_broken = True
    subpackage_names = ['']
