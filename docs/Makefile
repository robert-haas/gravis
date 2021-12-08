# Minimal makefile for Sphinx documentation

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

%:
	# Delete previous build
	@rm -rf build
	# Copy examples directory into docs source (required by nbsphinx to convert Jupyter notebooks into HTML)
	@-rm -rf source/code/examples
	@-mkdir -p source/code/
	@-cp -rf ../examples source/code/examples
	# Remove undesired items in examples directory
	@-find source/code/examples -name ".ipynb_checkpoints" -type d -exec rm -rf {} \; 2> /dev/null || true
	# Copy README.rst into docs source and modify its header to become package_references.rst
	@-echo "Package references" > source/rst/package_references.rst
	@-echo "==================" >> source/rst/package_references.rst
	@-tail -n +3 ../README.rst >> source/rst/package_references.rst
	# Build the docs
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# Modify RTD-theme so that it has no require.js redefinition and does not cause downstream errors
	# Also change the css to allow normal looking lists
	cp -f rtd_theme_modified/theme.js build/html/_static/js/theme.js
	cp -f rtd_theme_modified/theme.css build/html/_static/css/theme.css
	# Remove doctrees folder that is not needed for HTML representation
	@-rm -rf build/doctrees
	# Remove examples directory from docs source
	@-rm -rf source/code/examples
