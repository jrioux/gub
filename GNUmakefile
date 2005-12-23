
default: all

all: linux mingw mac


# local.make should set the following variables:
#
#  LILYPOND_CVSDIR - a CVS HEAD working directory
#

include local.make


include $(LILYPOND_CVSDIR)/VERSION

LILYPOND_VERSION=$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_LEVEL)$(if $(strip $(MY_PATCH_LEVEL)),.$(MY_PATCH_LEVEL),)


INVOKE_DRIVER=python driver.py \
--package-version=$(LILYPOND_VERSION) \
--package-build=1 --platform $(1)\
$(LOCAL_DRIVER_OPTIONS)
INVOKE_XPM=python xpm-apt.py --platform $(1) 


BUILD_ALL=$(call INVOKE_DRIVER, $(1)) build all  && $(call INVOKE_XPM, $(1)) -t install all \
  && $(call INVOKE_DRIVER, $(1)) build all  && $(call INVOKE_XPM, $(1))  install all \
  && $(call INVOKE_DRIVER, $(1)) build-installer


download:
	$(call INVOKE_DRIVER, linux) download
	$(call INVOKE_DRIVER, darwin) download
	$(call INVOKE_DRIVER, mingw) download

linux:
	$(call BUILD_ALL, linux) 

mac:
	$(call INVOKE_DRIVER, darwin) build darwin-sdk
	$(call INVOKE_XPM, darwin) install darwin-sdk
	$(call BUILD_ALL, darwin) 

mingw:
	$(call INVOKE_DRIVER, mingw) build mingw-runtime w32api 
	$(call INVOKE_XPM, mingw) install mingw-runtime w32api
	$(call BUILD_ALL, mingw) 



realclean:
	rm -rf src target

distclean: realclean
	echo NOT rm -rf downloads

sources = GNUmakefile $(wildcard *.py specs/*.py)
TAGS: $(sources)
	etags $^

cyg-apt.py: cyg-apt.py.in specs/cpm.py
	sed -e "/@CPM@/r specs/cpm.py" -e "s/@CPM@//" < $< > $@
	chmod +x $@

test-cygwin: cyg-apt.py
	rm -f ~/.cyg-apt .cyg-apt
	rm -rf cygwin
	./cyg-apt.py setup
	./cyg-apt.py -x install cygwin
	./cyg-apt.py list

test-gub: cyg-apt.py
	rm -f ~/.cyg-apt .cyg-apt
	./cyg-apt.py --root=target/i686-mingw32/system --mirror=file://uploads setup --ini=file://uploads/setup.ini
	./cyg-apt.py list

gpm-install: test-gub
	-./cyg-apt.py install $$(./cyg-apt.py search .)
	mkdir -p target/i686-mingw32/status
	mkdir -p target/i686-mingw32/tools
	touch target/i686-mingw32/status/binutils-2.16.1-0-{untar,patch,configure,compile,install,package,clean}
	touch target/i686-mingw32/status/gcc-3.4.5-0-{untar,patch,configure,compile,install,package,clean}
