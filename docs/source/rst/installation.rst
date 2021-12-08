Installation
############

This page explains the installation of **gravis** and its optional dependencies
**Selenium** for static image exports and **Jupyter notebooks** for embedded visualizations.



gravis
======

This package is available on the
`Python Package Index (PyPI) <https://pypi.org>`__
under the name
`gravis <https://pypi.org/project/gravis>`__.
It can be installed with Python's default package manager
`pip <https://pypi.org/project/pip>`__:

.. code-block:: console

   $ pip install gravis

Further remarks:

- gravis is compatible with `Python 3.5 upwards <https://www.python.org/downloads>`_.
- Using an environment manager like
  `virtualenv <https://virtualenv.pypa.io>`__ or
  `conda <https://docs.conda.io>`__
  is often a good idea. Such tools allow to create a
  `virtual environment <https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments>`__
  into which pip can install the package in an isolated fashion instead of globally
  on your system. Thereby it does not interfere with the installation of other projects,
  which may require a different version of some shared dependency.



Optional: Selenium
==================

gravis requires
`Selenium <https://selenium-python.readthedocs.io/>`__
to export visualizations as static images in JPG, PNG and SVG format.
It can be installed in two steps:

1. `Selenium Python bindings <https://selenium-python.readthedocs.io/installation.html#installing-python-bindings-for-selenium>`__
   are available on the Python Package Index (PyPI) under the name
   `selenium <https://pypi.org/project/selenium/>`__.
   It can be installed with Python's default package manager
   `pip <https://pypi.org/project/pip>`__:

   .. code-block:: console

      $ pip install selenium

2. `Webbrowser and associated driver <https://selenium-python.readthedocs.io/installation.html#drivers>`__

   Selenium connects Python to a webbrowser via a suitable driver.
   Both the webbrowser and corresponding driver need to be
   installed manually. Two options are supported by gravis:

   - `Chrome <https://www.google.com/intl/en/chrome/>`__
     browser with
     `ChromeDriver <https://sites.google.com/chromium.org/driver/>`__
   - `Firefox <https://www.mozilla.org/firefox>`__
     browser with
     `geckodriver <https://github.com/mozilla/geckodriver/releases>`__

   Further remarks:

   - gravis uses Chrome by default, but Firefox can be chosen with an argument of the
     export functions.
   - The browser version and driver version need to be compatible.
   - The driver executable needs to be in a directory that is listed in the
     ``PATH`` environment variable of the operating system, so that Python can find it.
     This can be achieved by putting the executable in a directory that is already
     listed in the ``PATH`` environment variable, such as ``/usr/bin`` or ``/usr/local/bin``
     on Linux, or by putting the executable in another directory and adding it to ``PATH``,
     for example on Linux with an entry in the ``.bashrc`` file in the user directory.



Optional: Jupyter notebook
==========================

gravis requires
`Jupyter notebook <https://jupyter.org>`__
for displaying graphs inline in notebooks in form of embedded HTML visualizations,
accompanied by Python code and Markdown comments.
A notebook is a file ending with ``.ipynb``, which can be created, modified and
executed with the
`notebook server <https://jupyter-notebook.readthedocs.io/en/stable/notebook.html#starting-the-notebook-server>`__
and a webbrowser opened by it. Jupyter notebook can be installed according
to its `recommended installation <https://jupyter.org/install>`__
with the package manager `conda <https://docs.conda.io>`__
from channel `conda-forge <https://anaconda.org/conda-forge/notebook>`__:

.. code-block:: console

   $ conda install -y -c conda-forge notebook

Further remarks:

- **Caution**: Some plots may not show up in the notebook with default settings.
  Instead only a blank area is visible. The reason is a parameter called
  ``iopub_data_rate_limit`` in Jupyter's
  `config system <https://jupyter-notebook.readthedocs.io/en/stable/config.html>`__.
  Its value `is chosen rather low by default <https://github.com/jupyter/notebook/issues/2287>`__.
  Plots that contain much data can therefore be blocked.
  This problem can be solved by increasing the value of the parameter,
  which can be done in two ways:
  
  1. Permanently change it with a config file in the directory ``~/.jupyter`` or
  2. Temporarily change it when opening a notebook by adding an optional argument
     to the start-up command:

     .. code-block:: console

        $ jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e12
