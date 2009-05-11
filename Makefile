# Targets
.PHONY: test clean docs ghdocs nosetests run syncdb

# Adds current work directory to ``PYTHONPATH``
PYTHONPATH=`pwd`

# ``tddspry`` related variables
project=tddspry
version=`python -c "import tddspry; print tddspry.get_version()"`

docs_dir=$(TMPDIR)/$(project)-docs
settings=testproject.settings
test_settings=testproject.settings

test: clean nosetests

clean:
	-find . -name '*.pyc' -exec rm {} \;
	-rm testproject/test.db

docs:
	$(MAKE) -C docs html

ghdocs:
	rm -rf $(docs_dir)
	$(MAKE) -C docs html
	cp -r docs/_build/html $(docs_dir)
	mv $(docs_dir)/_static $(docs_dir)/static
	mv $(docs_dir)/_sources $(docs_dir)/sources
	perl -pi -e "s/_sources/sources/g;" $(docs_dir)/*.html
	perl -pi -e "s/_static/static/g;" $(docs_dir)/*.html
	git checkout gh-pages
	rm -r sources static
	cp -rf $(docs_dir)/* .
	git add .
	git commit -a -m 'Updates $(project) documentation.'
	git checkout master
	rm -rf $(docs_dir)

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
