"""Simple and centralized access to web-related functionality."""

import base64 as _base64
import os as _os

from .args import check_arg as _check_arg


def image_to_html_element(location, name=None, width=None, height=None, unit='px',
                          data_format=None):
    """Convert an image file or URL to a self-contained HTML element with base64 encoded data.

    Parameters
    ----------
    data : str
        Filepath or URL of an image.
    name : str, optional
        Name shown if the image can not be shown in the browser.
    width : int, optional
        Width of the HTML element in pixels.
    height : int, optional
        Height of the HTML element in pixels.
    unit : str, optional
        Unit for width and height parameters.

        Available options: See
        `CSS values and units <https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Values_and_units>`__
    data_format : str, optional
        By default, the format of the image data is guessed from the file or URL
        ending of the ``location`` argument, or if that fails, from features of the
        binary data. Alternatively, the format can be passed explicitly with this argument,
        so no potentially incorrect guessing has to be done.

    Returns
    -------
    html_element : str
        A suitable HTML element for the image format that contains the data in form
        of a data URL.

    References
    ----------
    - MDN:
      `img <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img>`__,
      `a <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a>`__

    """
    # Argument processing
    known_formats = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'pdf', 'ps', 'eps']
    _check_arg(location, 'location', str)
    _check_arg(name, 'name', str, allow_none=True)
    _check_arg(width, 'width', int, allow_none=True)
    _check_arg(height, 'height', int, allow_none=True)
    _check_arg(unit, 'unit', str, allow_none=True)
    _check_arg(data_format, 'data_format', str, known_formats, allow_none=True)

    # Image to data URL
    data_url, data_format = image_to_data_url(location, data_format, return_data_format=True)

    # Embed data URL into a suitable HTML element
    if data_format in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
        html_element = url_to_img_element(data_url, name, width, height, unit)
    else:
        if not name:
            name = 'image.{}'.format(data_format)
        html_element = url_to_href_element(data_url, name)
    return html_element


def image_to_data_url(location, data_format=None, return_data_format=False):
    """Convert an image file or URL to a data URL with base64 encoded data.

    Parameters
    ----------
    data : str
        Filepath or URL of an image.
    data_format : str, optional
        By default, the format of the image data is guessed from the file or URL
        ending of the ``location`` argument, or if that fails, from features of the
        binary data. Alternatively, the format can be passed explicitly with this argument,
        so no potentially incorrect guessing has to be done.
    return_data_format : bool
        If True, the given or detected data format is returned in addition to the data url.

    Returns
    -------
    data_url : str
        URL with image data embedded inside it in form of text that represents
        base64 encoded binary data.

    References
    ----------
    - Wikipedia: `data URI scheme <https://en.wikipedia.org/wiki/Data_URI_scheme>`__
    - MDN: `Data URLs <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs>`__

    """
    # Argument processing
    known_formats = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'pdf', 'ps', 'eps']
    _check_arg(location, 'location', str)
    _check_arg(data_format, 'data_format', str, known_formats, allow_none=True)

    # Read data
    try:
        data = read_data(location)
    except Exception as excp:
        msg = 'Could not retrieve data from the given location.'
        raise ValueError(msg) from excp

    # Identify format
    if data_format is None:
        data_format = detect_format_from_location(location)
        if data_format is None:
            data_format = detect_format_from_data(data)
            if data_format is None:
                msg = (
                    'Could not auto-detect the image format from the given location or data. '
                    'You can provide it explicitly with the argument "data_format".')
                raise ValueError(msg) from None
    if data_format == 'jpg':
        data_format = 'jpeg'

    # Convert data to data URL
    base64_text = binary_data_to_base64_text(data)
    data_url = base64_text_to_data_url(base64_text, data_format)

    # Embed the data URL into a HTML element suited for the data format
    if return_data_format:
        return data_url, data_format
    return data_url


def read_data(location):
    """Read data from a location, which may be a filepath or an URL."""
    if _os.path.isfile(location):
        data = read_binary_file(location)
    else:
        data = read_url(location)
    return data


def read_binary_file(filepath):
    """Read the contents of a binary file."""
    with open(filepath, 'rb') as file_handle:
        data = file_handle.read()
    return data


def read_url(url):
    """Send a GET request to a given URL and read the response.

    References
    ----------
    - https://docs.python.org/3/howto/urllib2.html
    - https://docs.python.org/3/library/http.client.html#httpresponse-objects

    """
    import urllib.request

    with urllib.request.urlopen(url) as response:
        if response.status != 200:
            raise ConnectionError(response.reason)
        html = response.read()
    return html


def detect_format_from_location(location):
    """Try to detect the format from the given location and return None if it fails."""
    fmt = None
    location_lower = location.lower()
    known_formats = ['jpeg', 'jpg', 'png', 'gif', 'webp', 'svg', 'pdf', 'eps', 'ps']
    for candidate in known_formats:
        if location_lower.endswith(candidate):
            fmt = candidate
            break
    return fmt


def detect_format_from_data(data):
    """Try to detect the format of the given binary data and return None if it fails."""
    fmt = None
    try:
        if b'<svg' in data[:500]:
            fmt = 'svg'
        elif data.startswith(b'%PDF'):
            fmt = 'pdf'
        elif data.startswith(b'%!PS'):
            if b'EPS' in data[:100]:
                fmt = 'eps'
            else:
                fmt = 'ps'
        else:
            import imghdr

            fmt = imghdr.what(file=None, h=data)
            assert fmt is not None
    except Exception:
        pass
    return fmt


def binary_data_to_base64_text(binary_data):
    """Convert binary data to text data in Base64 format."""
    return _base64.b64encode(binary_data).decode('utf-8').replace('\n', '')


def base64_text_to_data_url(base64_text, data_format):
    """Convert data in form of base64 text to a data URL with suitable prefix."""
    # Argument processing
    if data_format == 'jpg':
        data_format = 'jpeg'

    # Transformation
    # - MIME type
    if data_format in ['jpeg', 'png', 'gif', 'webp']:
        mime_type = 'image/' + data_format
    elif data_format == 'svg':
        mime_type = 'image/svg+xml'
    elif data_format == 'pdf':
        mime_type = 'application/pdf'
    elif data_format in ['eps', 'ps']:
        mime_type = 'application/postscript'
    else:
        msg = 'Unknown data format. Can not assign a suitable MIME type.'
        raise ValueError(msg)
    # - Data URL
    data_url = 'data:{};base64,{}'.format(mime_type, base64_text)
    return data_url


def url_to_img_element(url, name, width, height, unit='px'):
    """Convert a given URL to a HTML img element."""
    style = None
    if width is not None and height is not None:
        style = 'width:{width}{unit};height:{height}{unit};'.format(
            width=width, height=height, unit=unit)
    elif width is not None:
        style = 'width:{width}{unit};'.format(width=width, unit=unit)
    elif height is not None:
        style = 'height:{height}{unit};'.format(height=height, unit=unit)

    html = '<img src="{}"'.format(url)
    if name is not None:
        html += ' alt="{}"'.format(name)
    if style is not None:
        html += ' style="{}"'.format(style)
    html += '>'
    return html


def url_to_href_element(url, name):
    """Convert a given URL to a HTML href element."""
    template = '<a href="{}">{}</a> '
    return template.format(url, name)
