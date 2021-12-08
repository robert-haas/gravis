"""Automatic index generation with a class that extends autosummary.

References
----------
- https://stackoverflow.com/questions/48074094/use-sphinx-autosummary-recursively-to-generate-api-documentation
- https://stackoverflow.com/questions/20569011/python-sphinx-autosummary-automated-listing-of-member-functions

"""

import re
from sphinx.ext.autosummary import Autosummary, get_documenter
from docutils.parsers.rst import directives
from sphinx.util.inspect import safe_getattr


class AutoAutoSummary(Autosummary):
    option_spec = {
        'methods': directives.unchanged,
        'attributes': directives.unchanged
    }
    required_arguments = 1

    @staticmethod
    def get_members(obj, typ, include_public=None):
        if not include_public:
            include_public = []
        items = []
        for name in dir(obj):
            try:
                documenter = get_documenter(safe_getattr(obj, name), obj)
            except AttributeError:
                continue
            if documenter.objtype == typ:
                items.append(name)
        public = [x for x in items if x in include_public or not x.startswith('_')]
        return public, items

    def run(self):
        clazz = str(self.arguments[0])
        try:
            (module_name, class_name) = clazz.rsplit('.', 1)
            m = __import__(module_name, globals(), locals(), [class_name])
            c = getattr(m, class_name)
            if 'methods' in self.options:
                _, methods = self.get_members(c, 'method', ['__init__'])

                self.content = ["~%s.%s" % (clazz, method) for method in methods if not method.startswith('_')]
            if 'attributes' in self.options:
                _, attribs = self.get_members(c, 'attribute')
                self.content = ["~%s.%s" % (clazz, attrib) for attrib in attribs if not attrib.startswith('_')]
        finally:
            return super(AutoAutoSummary, self).run()
