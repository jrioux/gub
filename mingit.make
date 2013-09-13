# -*-Makefile-*-

PACKAGE = git
ALL_PLATFORMS=mingw

MINGIT_BRANCH_FILEIFIED=$(subst /,--,$(MINGIT_BRANCH))
MINGIT_LOCAL_BRANCH=$(MINGIT_BRANCH_FILEIFIED)-repo.or.cz-git-mingw.git

default: all

PLATFORMS = mingw

include gub.make
include compilers.make

GPKG_OPTIONS=--branch git=$(MINGIT_LOCAL_BRANCH)

GUB_OPTIONS=\
 --branch git=$(MINGIT_BRANCH):$(MINGIT_LOCAL_BRANCH)

INSTALLER_BUILDER_OPTIONS=\
  --branch=git=$(MINGIT_LOCAL_BRANCH)\
  --version-db=versiondb/git.versions \

all: $(PLATFORMS)

download: download-mingit

download-mingit:
	$(MAKE) -f mingit.make update-versions

mingw:
	$(call BUILD,$@,git)

update-versions:
	$(PYTHON) gub/versiondb.py --no-sources --url http://lilypond.org/git --dbfile versiondb/git.versions --download --platforms="$(PLATFORMS)"

LAST_GIT=$(shell ls -1 -t uploads/git*.exe|head -1)
TAG=gub-release-mingw-git-$(subst uploads/git-,,$(LAST_GIT))
upload:
	rsync --delay-updates -v --progress $(LAST_GIT) hanwen@lilypond.org:www/git/binaries/mingw/
	$(MAKE) -f mingit.make update-versions
	git tag $(TAG)
	git push ssh+git://git.sv.gnu.org/srv/git/lilypond.git $(TAG):refs/tags/$(TAG)

