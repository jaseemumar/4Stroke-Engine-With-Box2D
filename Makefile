.SUFFIXES: .cpp .hpp

# Programs
SHELL 	= bash
CC     	= g++
LD	= ld
RM 	= rm
ECHO	= /bin/echo
CAT	= cat
PRINTF	= printf
SED	= sed
DOXYGEN = doxygen
######################################
# Project Name (generate executable with this name)
TARGET = cs296_base

# Project Paths
PROJECT_ROOT=./
EXTERNAL_ROOT=$(PROJECT_ROOT)/external
SRCDIR = $(PROJECT_ROOT)/src
OBJDIR = $(PROJECT_ROOT)/obj
BINDIR = $(PROJECT_ROOT)/bin
DOCDIR = $(PROJECT_ROOT)/doc
DATADIR = $(PROJECT_ROOT)/data

# Library Paths
BOX2D_ROOT=$(EXTERNAL_ROOT)
GLUI_ROOT=/usr
GL_ROOT=/usr/include/

#Libraries
LIBS = -lBox2D -lglui -lglut -lGLU -lGL

# Compiler and Linker flags
CPPFLAGS =-g -O3 -Wall -fno-strict-aliasing
CPPFLAGS+=-I $(BOX2D_ROOT)/include -I $(GLUI_ROOT)/include
LDFLAGS+=-L $(BOX2D_ROOT)/lib -L $(GLUI_ROOT)/lib

######################################

NO_COLOR=\e[0m
OK_COLOR=\e[1;32m
ERR_COLOR=\e[1;31m
WARN_COLOR=\e[1;33m
MESG_COLOR=\e[1;34m
FILE_COLOR=\e[1;37m

OK_STRING="[OK]"
ERR_STRING="[ERRORS]"
WARN_STRING="[WARNINGS]"
OK_FMT="${OK_COLOR}%30s\n${NO_COLOR}"
ERR_FMT="${ERR_COLOR}%30s\n${NO_COLOR}"
WARN_FMT="${WARN_COLOR}%30s\n${NO_COLOR}"
######################################

SRCS := $(wildcard $(SRCDIR)/*.cpp)
INCS := $(wildcard $(SRCDIR)/*.hpp)
OBJS := $(SRCS:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)


.PHONY: all setup doc clean distclean install

all:setup $(BINDIR)/$(TARGET) doc report

setup:
	@$(ECHO) "Setting up compilation..."
	@mkdir -p obj
	@mkdir -p bin
	@mkdir -p data

$(BINDIR)/$(TARGET): $(OBJS)
	@$(PRINTF) "$(MESG_COLOR)Building executable:$(NO_COLOR) $(FILE_COLOR) %16s$(NO_COLOR)" "$(notdir $@)"
	@$(CC) -pg -o $@ $(LDFLAGS) $(OBJS) $(LIBS) 2> temp.log || touch temp.err
	@if test -e temp.err; \
	then $(PRINTF) $(ERR_FMT) $(ERR_STRING) && $(CAT) temp.log; \
	elif test -s temp.log; \
	then $(PRINTF) $(WARN_FMT) $(WARN_STRING) && $(CAT) temp.log; \
	else $(PRINTF) $(OK_FMT) $(OK_STRING); \
	fi;
	@$(RM) -f temp.log temp.err

-include -include $(OBJS:.o=.d)

$(OBJS): $(OBJDIR)/%.o : $(SRCDIR)/%.cpp
	@$(PRINTF) "$(MESG_COLOR)Compiling: $(NO_COLOR) $(FILE_COLOR) %25s$(NO_COLOR)" "$(notdir $<)"
	@$(CC) -pg $(CPPFLAGS) -c $< -o $@ -MD 2> temp.log || touch temp.err
	@if test -e temp.err; \
	then $(PRINTF) $(ERR_FMT) $(ERR_STRING) && $(CAT) temp.log; \
	elif test -s temp.log; \
	then $(PRINTF) $(WARN_FMT) $(WARN_STRING) && $(CAT) temp.log; \
	else printf "${OK_COLOR}%30s\n${NO_COLOR}" "[OK]"; \
	fi;
	@$(RM) -f temp.log temp.err

doc:
	@$(ECHO) -n "Generating Doxygen Documentation ...  "
	@$(RM) -rf doc/html
	@$(DOXYGEN) $(DOCDIR)/Doxyfile 2 > /dev/null
	@$(ECHO) "Done"

clean:
	@$(ECHO) -n "Cleaning up..."
	@$(RM) -rf $(OBJDIR) $(BINDIR) *~ $(DEPS) $(SRCDIR)/*~
	@$(ECHO) "Done"

distclean: clean
	@$(RM) -rf $(BINDIR) $(DOCDIR)/html
	@$(RM) -f $(DATADIR)/*.aux $(DATADIR)/*.log $(DATADIR)/*.dvi $(DATADIR)/*.bbl $(DATADIR)/*.blg $(DATADIR)/*.pdf
	
uninstall: distclean
	@echo "uninstalling ..."
	@rm -rf $(EXTERNAL_ROOT)/include/* $(EXTERNAL_ROOT)/lib/*  $(EXTERNAL_ROOT)/src/Box2D
	@rm -rf $(DOCDIR)/g20_project_htmlreport
	@rm -f gmon.out
	

#add documentaion and g20_project_report tag to install

install: setup
	@if ! test -d $(EXTERNAL_ROOT)/include/Box2D;\
	then cd $(EXTERNAL_ROOT)/src;\
	tar -xvzf Box2D.tgz;\
	cd Box2D;\
	mkdir build296;\
	cd build296;\
	cmake -DCMAKE_BUILD_TYPE=Release ../ ;\
	make ;\
	make install;\
	fi;
	
	
dist:distclean
	@tar -cvzf ../cs296_g20_project.tar.gz ../cs296_base_code
	
report: 
	@echo "Generating g20_project_report ..."
	@cd $(DATADIR) && latex g20_project_report &&	bibtex g20_project_report &&		latex g20_project_report &&	latex g20_project_report &&	latex g20_project_report && pdflatex g20_project_report
	@$(RM) -f $(DATADIR)/*.aux $(DATADIR)/*.bbl $(DOCDIR)/*.blg $(DATADIR)/*.log $(DATADIR)/*.dvi
