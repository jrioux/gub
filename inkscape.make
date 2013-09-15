.PHONY: all gub3-packages gub3-installers
.PHONY: inkscape inkscape-installer inkscape-installers print-success

all: inkscape inkscape-installer print-success

include gub.make


INKSCAPE_BRANCH=trunk?revision=22714
INKSCAPE_REPO_URL=svn:http://svn.code.sf.net/p/inkscape/code/inkscape

PLATFORMS=linux-x86
# Cocoa/Carbon?
# PLATFORMS+=darwin-ppc darwin-x86
PLATFORMS+=mingw
PLATFORMS+=linux-64
PLATFORMS+=linux-ppc
PLATFORMS+=freebsd-x86 freebsd-64
#PLATFORMS+=cygwin

#derived info
INKSCAPE_SOURCE_URL=$(INKSCAPE_REPO_URL)?branch=$(INKSCAPE_BRANCH)
INKSCAPE_DIRRED_BRANCH=$(shell $(PYTHON) gub/repository.py --branch-dir '$(INKSCAPE_SOURCE_URL)')
INKSCAPE_FLATTENED_BRANCH=$(shell $(PYTHON) gub/repository.py --full-branch-name '$(INKSCAPE_SOURCE_URL)')

BUILD_PACKAGE='$(INKSCAPE_SOURCE_URL)'
INSTALL_PACKAGE = inkscape

INSTALLER_BUILDER_OPTIONS =\
 --version-db=versiondb/inkscape.versions\
 $(if $(INKSCAPE_BRANCH), --branch=blinkscape=$(INKSCAPE_FLATTENED_BRANCH),)\
 $(if $(INKSCAPE_BRANCH), --branch=inkscape=trunk,)\
#

MAKE += -f inkscape.make

inkscape: packages

inkscape-installer: installers
inkscape-installers: installers

update-versions:
	python gub/versiondb.py --no-sources --version-db=versiondb/inkscape.versions --download --platforms="mingw" --url=http://lilypond.org/blog/janneke/software/inkscape

print-success:
	@echo installer: uploads/inkscape*$(BUILD_PLATFORM).sh

print-branches:
	@echo "--branch=inkscape=$(INKSCAPE_FLATTENED_BRANCH)"
