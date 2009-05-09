# Copyright (C) 2001-2009 KDS Software Group http://www.kds.com.ua/

include Makefile.def

# Targets
.PHONY: test clean docs nosetests run syncdb

test: clean nosetests

clean:
	-find . -name '*.pyc' -exec rm {} \;
	-rm testproject/test.db

docs:
	$(MAKE) -C docs html

nosetests:
	PYTHONPATH=$(PYTHONPATH) ./bin/django-nosetests.py --with-django-settings=$(test_settings) -w .. --with-coverage --cover-package=tddspry --exe testproject

run:
	PYTHONPATH=$(PYTHONPATH) python testproject/manage.py runserver

syncdb:
	PYTHONPATH=$(PYTHONPATH) python testproject/manage.py syncdb

### Local variables: ***
### compile-command:"make" ***
### tab-width: 2 ***
### End: ***
