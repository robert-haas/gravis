import os

import pytest


# conftest.py is automatically detected by pytest

# 1) Define a command line argument for outdir that is made available to tests via a fixture
# - https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions

def pytest_addoption(parser):
    parser.addoption("--my-outdir", action="store", default="output")


@pytest.fixture(scope='session')
def my_outdir(request):
    outdir = request.config.option.my_outdir
    if outdir is None:
        pytest.skip()
    else:
        try:
            os.mkdir(outdir)
        except Exception:
            pass
    return outdir


# 2) Register a custom marker and use it to skip certain tests depending on graph library installs
# (used in tox system tests to remove a lot of C++ dependencies)
# - http://doc.pytest.org/en/latest/mark.html#registering-marks
# - http://doc.pytest.org/en/latest/example/markers.html#marking-test-functions-and-selecting-them-for-a-run
def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'only_with_graph_libraries: mark test to run only when graph libraries are installed')
    config.addinivalue_line(
        'markers',
        'only_with_selenium: mark test to run only when Selenium is installed')
