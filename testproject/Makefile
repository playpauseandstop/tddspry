# Copyright (C) 2001-2009 KDS Software Group http://www.kds.com.ua/

include ../Makefile.def

noseopt=-w .. --with-coverage --cover-package=tddspry --exe
modules=testproject

.PHONY: clean test

clean:
	-rm test.db

test:
	PYTHONPATH=$(PYTHONPATH):. DJANGO_SETTINGS_MODULE=$(test_settings) nosetests  $(noseopt) $(modules)

### Local variables: ***
### compile-command:"make" ***
### tab-width: 2 ***
### End: ***
