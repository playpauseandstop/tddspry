# Targets
.PHONY: alltest clean distclean manage runserver shell smarttest syncdb test test_multidb test_mysql test_sqlite

# Initial vars
errors=errors
nosetests=PYTHONPATH=.. `pwd`/../bin/django-nosetests.py
python=PYTHONPATH=.. python
project=testproject

manage=$(python) $(project)/manage.py
settings=$(project).settings

# Settings for ``distclean`` target
VENV?=env*

# Settings for ``runserver`` target
IP?=0.0.0.0
PORT?=8191

# Settings for ``test`` target
TEST?=$(project)
TEST_ARGS?=-x
TEST_ARGS_MULTIDB?=-e multidb
TEST_SETTINGS?=$(settings)
TWILL_ERROR_DIR?=$(errors)

all: test
alltest: smarttest test test_multidb test_mysql test_sqlite

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
	$(nosetests) $(TEST_ARGS) $(TEST_ARGS_MULTIDB) --twill-error-dir=$(TWILL_ERROR_DIR) $(TEST)

syncdb:
	$(manage) syncdb --noinput

test: clean
	$(nosetests) $(TEST_ARGS) $(TEST_ARGS_MULTIDB) --django-settings=$(TEST_SETTINGS) --twill-error-dir=$(TWILL_ERROR_DIR) $(TEST)

test_multidb:
	TEST_ARGS_MULTIDB= TEST_SETTINGS=$(settings)_multidb $(MAKE) test

test_mysql: clean
	TEST_SETTINGS=$(settings)_mysql $(MAKE) test

test_sqlite: clean
	TEST_SETTINGS=$(settings)_sqlite $(MAKE) test
