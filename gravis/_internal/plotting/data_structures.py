"""Data structures for representing JavaScript plots."""

import random as _random
import string as _string

from ..utils import operating_system as _operating_system
from . import rendering, template_system


class Figure:
    """Data structure for wrapping, displaying and exporting a JavaScript figure."""

    def __init__(self, html_template):
        """Initialize a figure with a partly filled HTML template containing a visualization."""
        self._html_template = html_template

    # IPython integration
    def _repr_html_(self):
        """Provide HTML text for integration with IPython rich display representation.

        References
        ----------
        - https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display
        - https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.formatters.html#IPython.core.formatters.HTMLFormatter

        """
        return self.to_html_partial()

    # Display in browser or notebook
    def display(self, inline=False):
        """Display the plot in a webbrowser or as IPython rich display representation.

        Parameters
        ----------
        inline : bool
            If True, the plot will be shown inline in a Jupyter notebook.

        """
        if inline:
            import IPython

            html_text = self.to_html_partial()
            html_object = IPython.display.HTML(html_text)
            IPython.display.display(html_object)
        else:
            html_text = self.to_html_standalone()
            _operating_system.open_in_webbrowser(html_text)

    # Representation as text
    def to_html(self):
        """Create a HTML text representation."""
        return self.to_html_standalone()

    def to_html_standalone(self):
        """Create a standalone HTML text representation that has all javascript code embedded."""
        data = {
            'RANDOM_ID': self._generate_random_id(),
            'PREFIX': """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="margin:0;">""",
            'LOAD_REQUIRE': template_system.load('third_party/require/require.min.js'),
            'SUFFIX': """</body>
</html>""",
        }
        html_text = template_system.insert(self._html_template, data)
        return html_text

    def to_html_partial(self):
        """Create a dependent HTML text representation that loads javascript with require.js."""
        data = {
            'RANDOM_ID': self._generate_random_id(),
            'PREFIX': '',
            'LOAD_REQUIRE': template_system.load('third_party/require/require.min.js'),
            'SUFFIX': '',
        }
        html_text = template_system.insert(self._html_template, data)
        return html_text

    def to_jpg(self, webdriver='chrome', capture_delay=3.5):
        """Create a JPEG text representation with base64 text encoding the binary data."""
        html_text = self.to_html()
        jpg_data = rendering.render_and_capture(html_text, 'jpg', webdriver, capture_delay)
        return jpg_data

    def to_png(self, webdriver='chrome', capture_delay=3.5):
        """Create a PNG text representation with base64 text encoding the binary data."""
        html_text = self.to_html()
        png_data = rendering.render_and_capture(html_text, 'png', webdriver, capture_delay)
        return png_data

    def to_svg(self, webdriver='chrome', capture_delay=3.5):
        """Create a SVG text representation."""
        html_text = self.to_html()
        svg_text = rendering.render_and_capture(html_text, 'svg', webdriver, capture_delay)
        return svg_text

    # Export as HTML file
    def export_html(self, filepath, overwrite=False):
        """Export the plot as HTML file.

        Parameters
        ----------
        filepath : str
            Filepath for the generated HTML file.
        overwrite : bool
            If True, overwrite the file if it already exists.

        Raises
        ------
        FileExistsError
            If overwrite=False and there is already a file at the given filepath.

        """
        # Precondition
        if not overwrite:
            _operating_system.is_file(filepath, raise_exception=True)

        # Transformation
        with open(filepath, 'w') as file_handle:
            html_text = self.to_html()
            file_handle.write(html_text)

    def export_svg(self, filepath, overwrite=False, webdriver='chrome', capture_delay=3.5):
        """Export the plot as SVG file.

        Parameters
        ----------
        filepath : str
            Filepath for the generated SVG file.
        overwrite : bool
            If True, overwrite the file if it already exists.

        Raises
        ------
        FileExistsError
            If overwrite=False and there is already a file at the given filepath.

        """
        # Precondition
        if not overwrite:
            _operating_system.is_file(filepath, raise_exception=True)

        # Transformation
        with open(filepath, 'w') as file_handle:
            svg_text = self.to_svg(webdriver, capture_delay)
            file_handle.write(svg_text)

    def export_png(self, filepath, overwrite=False, webdriver='chrome', capture_delay=3.5):
        """Export the plot as PNG file.

        Parameters
        ----------
        filepath : str
            Filepath for the generated PNG file.
        overwrite : bool
            If True, overwrite the file if it already exists.

        Raises
        ------
        FileExistsError
            If overwrite=False and there is already a file at the given filepath.

        """
        # Precondition
        if not overwrite:
            _operating_system.is_file(filepath, raise_exception=True)

        # Transformation
        with open(filepath, 'wb') as file_handle:
            png_text = self.to_png(webdriver, capture_delay)
            file_handle.write(png_text)

    def export_jpg(self, filepath, overwrite=False, webdriver='chrome', capture_delay=3.5):
        """Export the plot as JPEG file.

        Parameters
        ----------
        filepath : str
            Filepath for the generated JPEG file.
        overwrite : bool
            If True, overwrite the file if it already exists.

        Raises
        ------
        FileExistsError
            If overwrite=False and there is already a file at the given filepath.

        """
        # Precondition
        if not overwrite:
            _operating_system.is_file(filepath, raise_exception=True)

        # Transformation
        with open(filepath, 'wb') as file_handle:
            jpg_text = self.to_jpg(webdriver, capture_delay)
            file_handle.write(jpg_text)

    @staticmethod
    def _generate_random_id(length=16):
        """Generate a random identifier starting with "i and consisting of letters and digits."""
        symbols = _string.ascii_letters + _string.digits
        return 'i' + ''.join(_random.choice(symbols) for _ in range(length))
