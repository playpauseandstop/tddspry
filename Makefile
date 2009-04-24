# Copyright (C) 2001-2009 KDS Software Group http://www.kds.com.ua/

include Makefile.def

# Targets
.PHONY: test clean nosetests run syncdb

test: clean nosetests

clean:
	$(MAKE) -C testproject clean
	-find . -name '*.pyc' -exec rm {} \;

nosetests:
	$(MAKE) -C testproject test

run:
	PYTHONPATH=$(PYTHONPATH) python testproject/manage.py runserver

syncdb:
	PYTHONPATH=$(PYTHONPATH) python testproject/manage.py syncdb

### Local variables: ***
### compile-command:"make" ***
### tab-width: 2 ***
### End: ***
