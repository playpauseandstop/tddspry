# Targets
.PHONY: alltest clean distclean manage runserver shell smarttest syncdb test test_django_nose test_multidb test_mysql test_sqlite

# Initial vars
python=PYTHONPATH=.. python -W ignore::DeprecationWarning

errors=errors
nosetests=$(python) `pwd`/../bin/django-nosetests.py
project=testproject

manage=$(python) $(project)/manage.py
settings=$(project).settings

# Read Django and tddspry versions
DJANGO_VERSION=`$(python) -c 'import django; print(django.get_version());'`
DJANGO_VERSION_SHORT=`$(python) -c 'import django; print(django.get_version());' | cut -b 1-3`
TDDSPRY_VERSION=`$(python) -c 'import tddspry; print(tddspry.get_version());'`

# Settings for ``distclean`` target
VENV?=env*

# Settings for ``runserver`` target
IP?=0.0.0.0
PORT?=8191

# Settings for ``test`` target
TEST?=$(project)
TEST_ARGS?=-x
TEST_ARGS_DATADIFF?=-e datadiff
TEST_ARGS_MULTIDB?=-e multidb
TEST_SETTINGS?=$(settings)
export TWILL_ERROR_DIR?=$(errors)

all: test
alltest: smarttest test test_datadiff test_django_nose test_multidb test_mysql test_sqlite

clean:
	find . -name '*.pyc' -delete

distclean: clean
	find . -name 'pip-log.txt' -delete
	rm -rf $(VENV)/
	rm -f $(project).db

manage:
	$(manage) $(COMMAND)

runserver:
	$(manage) runserver $(IP):$(PORT)

shell:
	COMMAND=shell $(MAKE) manage

smarttest: clean
	$(nosetests) $(TEST_ARGS) $(TEST_ARGS_DATADIFF) $(TEST_ARGS_MULTIDB) --twill-error-dir=$(TWILL_ERROR_DIR) $(TEST)

syncdb:
	$(manage) syncdb --noinput

test: clean
	$(nosetests) $(TEST_ARGS) $(TEST_ARGS_DATADIFF) $(TEST_ARGS_MULTIDB) --django-settings=$(TEST_SETTINGS) $(TEST)

test_datadiff: clean
	TEST_ARGS_DATADIFF= TEST_SETTINGS=$(settings)_datadiff $(MAKE) test

test_django_nose: clean
	RUNNING_TEST=yes test $(DJANGO_VERSION_SHORT) = "1.0" -o $(DJANGO_VERSION_SHORT) = "1.1" && echo "Django $(DJANGO_VERSION_SHORT) does not support testing via django-nose test suite runner." || $(manage) test $(TEST_ARGS) $(TEST)

test_multidb:
	test $(DJANGO_VERSION_SHORT) = "1.0" -o $(DJANGO_VERSION_SHORT) = "1.1" && echo "Django $(DJANGO_VERSION_SHORT) does not support multi database testing." || TEST_ARGS_MULTIDB= TEST_SETTINGS=$(settings)_multidb $(MAKE) test

test_mysql: clean
	TEST_SETTINGS=$(settings)_mysql $(MAKE) test

test_sqlite: clean
	TEST_SETTINGS=$(settings)_sqlite $(MAKE) test
