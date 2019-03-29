export TOP_DIR := $(shell git rev-parse --show-toplevel)

include $(TOP_DIR)/../bsg_idf_tools/Makefile.include

#===============================================================================
# Makefile
#
# While a majority of the design is here, there are a few last minute things we
# need to do. Therefore, you should run '$ make' in the design direcotry (where
# this makefile live) to update the design. Before using this makefile, you
# should make sure to do the following things (look for the TODOs):
#
# 	1. Update macro_generate.py for your process specific macro generator
# 	2. Update the hard/*.v files to instantiate your hardened modules
# 	3. Link your technology file (.tf) below for IDF to DEF conversion
#
#===============================================================================

# TODO: Set me to the path of your target process's technology (.tf) file
TECHNOLOGY_FILE ?=

# Create a list of all the verilog files in the hard directory
HARD_V_FILES :=$(shell find hard/ -name *.v)

#===============================================================================
# MAIN TARGETS
#===============================================================================

.DEFAULT_GOAL=all

all: macro_generate convert_idf_to_def
	@echo "All Done!"

macro_generate: tools
	$(PYTHON) macro_generate.py

convert_idf_to_def: floorplan.idf.json tools
	$(PYTHON) $(BASEJUMP_IDF_TOOLS_DIR)/idf_to_def/idf_to_def.py -idf $< -tf $(TECHNOLOGY_FILE)

