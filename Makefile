# Some manipulation with Sphinx-generated docs before sending it to GitHub.

all:
	rm -r sources static
	mv _sources sources
	mv _static static
	perl -pi -e "s/_sources/sources/g;" *.html
	perl -pi -e "s/_static/static/g;" *.html
