# Targets
.PHONY: clean docs fullclean fulltest ghdocs pypi test

# ``tddspry`` related variables
project=tddspry
docs_dir=$(TMPDIR)/$(project)-docs

clean:
	find . -name '*.pyc' -delete

docs:
	$(MAKE) -C docs html

fullclean: clean
	find . -name 'pip-log.txt' -delete
	rm -rf build/
	rm -rf dist/
	rm -rf docs/_build/
	rm -rf $(project).egg-info/
	rm -f MANIFEST
	-$(MAKE) -C testproject fullclean

fulltest:
	$(MAKE) -C testproject allfulltest

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

test:
	$(MAKE) -C testproject alltest

### Local variables: ***
### compile-command:"make" ***
### tab-width: 4 ***
### End: ***
