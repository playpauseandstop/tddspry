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

ghdocs:
	rm -rf $(TMPDIR)/tddspry-docs
	$(MAKE) -C docs html
	cp -r docs/_build/html $(TMPDIR)/tddspry-docs
	mv $(TMPDIR)/tddspry-docs/_static $(TMPDIR)/tddspry-docs/static
	mv $(TMPDIR)/tddspry-docs/_sources $(TMPDIR)/tddspry-docs/sources
	perl -pi -e "s/_sources/sources/g;" $(TMPDIR)/tddspry-docs/*.html
	perl -pi -e "s/_static/static/g;" $(TMPDIR)/tddspry-docs/*.html
	git checkout gh-pages
	rm -r sources static
	cp -rf $(TMPDIR)/tddspry-docs/* .
	git add .
	git commit -a -m 'Updates tddspry documentation.'
	git checkout master
	rm -rf $(TMPDIR)/tddspry-docs

nosetests:
	PYTHONPATH=$(PYTHONPATH) ./bin/django-nosetests.py --with-django-settings=$(test_settings) -w .. --with-coverage --cover-package=tddspry --exe testproject

run:
	PYTHONPATH=$(PYTHONPATH) ./testproject/manage.py runserver

syncdb:
	PYTHONPATH=$(PYTHONPATH) ./testproject/manage.py syncdb

### Local variables: ***
### compile-command:"make" ***
### tab-width: 2 ***
### End: ***
