# -*-Makefile-*-


ALL_PLATFORMS=mingw

PLATFORMS=$(ALL_PLATFORMS)

BRANCH_FILEIFIED=$(subst /,--,$(BRANCH))

GIT_LOCAL_BRANCH=$(BRANCH_FILEIFIED)-repo.or.cz-git-mingw.git
BRANCH=master

PYTHONPATH=lib/
export PYTHONPATH

PYTHON=python
OTHER_PLATFORMS=$(filter-out $(BUILD_PLATFORM), $(PLATFORMS))

INVOKE_GUP=$(PYTHON) gup-manager.py \
--platform $(1) \
--branch git=$(LILYPOND_LOCAL_BRANCH)

INVOKE_GUB_BUILDER=$(PYTHON) gub-builder.py \
--target-platform $(1) \
--branch git=$(BRANCH):$(GIT_LOCAL_BRANCH) \
$(foreach h,$(GUB_NATIVE_DISTCC_HOSTS), --native-distcc-host $(h))\
$(foreach h,$(GUB_CROSS_DISTCC_HOSTS), --cross-distcc-host $(h))\
$(LOCAL_GUB_BUILDER_OPTIONS)

INVOKE_INSTALLER_BUILDER=$(PYTHON) installer-builder.py \
  --target-platform $(1) \
  --branch git=$(GIT_LOCAL_BRANCH) \


BUILD=$(call INVOKE_GUB_BUILDER,$(1)) build $(2) \
  && $(call INVOKE_INSTALLER_BUILDER,$(1)) build-all git


default: all

all: $(PLATFORMS)

include compilers.make

download:
	$(foreach p, $(PLATFORMS), $(call INVOKE_GUB_BUILDER,$(p)) download git && ) true

bootstrap: bootstrap-git download-local local cross-compilers local-cross-tools download 

bootstrap-git:
	$(PYTHON) gub-builder.py $(LOCAL_GUB_BUILDER_OPTIONS) -p local download git
	$(PYTHON) gub-builder.py $(LOCAL_GUB_BUILDER_OPTIONS) -p local build git

download-local:
	$(PYTHON) gub-builder.py $(LOCAL_GUB_BUILDER_OPTIONS) -p local download \
		git pkg-config nsis icoutils 

local:
	$(PYTHON) gub-builder.py $(LOCAL_GUB_BUILDER_OPTIONS) -p local build \
		git 


mingw:
	$(call BUILD,$@,git)
