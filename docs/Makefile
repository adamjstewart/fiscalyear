# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINX_BUILD		?= sphinx-build
SPHINX_BUILD_OPTS	?= -W -j auto --keep-going
SOURCE_DIR		= .
BUILD_DIR		= _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINX_BUILD) -M help "$(SOURCE_DIR)" "$(BUILD_DIR)" $(SPHINX_BUILD_OPTS)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new "make mode" option.
%: Makefile
	@$(SPHINX_BUILD) -M $@ "$(SOURCE_DIR)" "$(BUILD_DIR)" $(SPHINX_BUILD_OPTS)
