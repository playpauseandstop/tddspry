# Targets
.PHONY: clean distclean docs ghdocs test

# Initial vars
project=tddspry

docs_dir=docs
tests_dir=tests
tmp_docs_dir=$(TMPDIR)/$(project)-docs

clean:
	find . -name '*.pyc' -delete
	-$(MAKE) -C $(docs_dir) clean
	-$(MAKE) -C $(tests_dir) clean

distclean: clean
	find . -name 'pip-log.txt' -delete
	rm -rf build/
	rm -rf dist/
	rm -rf $(project).egg-info/
	rm -f MANIFEST
	-$(MAKE) -C $(docs_dir) distclean
	-$(MAKE) -C $(tests_dir) distclean

docs:
	$(MAKE) -C $(docs_dir) html

ghdocs:
	rm -rf $(tmp_docs_dir)
	$(MAKE) docs
	cp -r $(docs)/_build/html $(docs_dir)
	mv $(docs_dir)/_static $(docs_dir)/static
	mv $(docs_dir)/_sources $(docs_dir)/sources
	perl -pi -e "s/_sources/sources/g;" $(docs_dir)/*.html
	perl -pi -e "s/_static/static/g;" $(docs_dir)/*.html
	git checkout gh-pages
	rm -r sources static
	cp -rf $(tmp_docs_dir)/* .
	git add .
	git commit -a -m 'Updates $(project) documentation.'
	git checkout master
	rm -rf $(tmp_docs_dir)

test:
	./$(tests_dir)/runtests.sh $(TEST)
