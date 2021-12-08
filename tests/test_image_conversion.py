import os

import pytest
import shared

import gravis as gv


def test_url():
    # svg
    url = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Infobox_info_icon.svg'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<img src="data:image/svg+xml;base64,')

    # jpg
    url = 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<img src="data:image/jpeg;base64,')

    # png
    url = 'https://upload.wikimedia.org/wikipedia/commons/5/53/Wikimedia-logo.png'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<img src="data:image/png;base64,')

    # webp
    url = 'https://upload.wikimedia.org/wikipedia/commons/c/cd/WebP-Gradient.webp'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<img src="data:image/webp;base64,')

    # gif static
    url = 'https://upload.wikimedia.org/wikipedia/commons/a/a0/Sunflower_as_gif_websafe.gif'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<img src="data:image/gif;base64,')

    # gif animated
    url = 'https://upload.wikimedia.org/wikipedia/commons/c/c8/132C_trans.gif'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<img src="data:image/gif;base64,')

    # pdf
    url = 'https://upload.wikimedia.org/wikipedia/commons/0/05/Discovery_Year_0-1-2.pdf'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<a href="data:application/pdf;base64,')

    # ps
    url = 'https://example-files.online-convert.com/vector%20image/ps/example.ps'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<a href="data:application/postscript;base64,')

    # eps
    url = 'https://example-files.online-convert.com/vector%20image/eps/example.eps'
    el = gv.convert.image_to_html_element(url)
    assert el.startswith('<a href="data:application/postscript;base64,')


def test_file_with_valid_extension():
    # svg
    filepath = 'rectangle_10x10.svg'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/svg+xml;base64,')

    # jpg
    filepath = 'rectangle_10x10.jpg'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/jpeg;base64,')

    # jpeg
    filepath = 'rectangle_10x10.jpeg'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/jpeg;base64,')

    # png
    filepath = 'rectangle_10x10.png'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/png;base64,')

    # webp
    filepath = 'rectangle_10x10.webp'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/webp;base64,')

    # gif
    filepath = 'rectangle_10x10.gif'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/gif;base64,')

    # pdf
    filepath = 'rectangle_10x10.pdf'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<a href="data:application/pdf;base64,')

    # ps
    filepath = 'rectangle_10x10.ps'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<a href="data:application/postscript;base64,')

    # eps
    filepath = 'rectangle_10x10.eps'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<a href="data:application/postscript;base64,')


def test_file_with_invalid_extension():
    # svg
    filepath = 'svg_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/svg+xml;base64,')

    # jpg
    filepath = 'jpg_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/jpeg;base64,')

    # jpeg
    filepath = 'jpeg_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/jpeg;base64,')

    # png
    filepath = 'png_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/png;base64,')

    # webp
    filepath = 'webp_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/webp;base64,')

    # gif
    filepath = 'gif_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<img src="data:image/gif;base64,')

    # pdf
    filepath = 'pdf_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<a href="data:application/pdf;base64,')

    # ps
    filepath = 'ps_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<a href="data:application/postscript;base64,')

    # eps
    filepath = 'eps_file'
    el = gv.convert.image_to_html_element(os.path.join(shared.IN_DIR, filepath))
    assert el.startswith('<a href="data:application/postscript;base64,')


def test_optional_arguments():
    filepath = os.path.join(shared.IN_DIR, 'rectangle_10x10.jpg')

    # width, height, unit, data_format
    combinations = [
        dict(width=30),
        dict(height=30),
        dict(unit='mm'),
        dict(data_format='jpg', name='alt_text'),
        dict(width=30, unit='cm', data_format='jpeg'),
        dict(width=30, height=30, data_format='jpeg'),
        dict(height=30, data_format='jpeg'),
    ]
    for kwargs in combinations:
        el = gv.convert.image_to_html_element(filepath, **kwargs)
        assert el.startswith('<img src="data:image/jpeg;base64,')

    # data_format
    for fmt in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'pdf', 'ps', 'eps']:
        el = gv.convert.image_to_html_element(filepath, data_format=fmt)
        if fmt == 'jpg':
            assert 'jpeg' in el[:200]
        elif fmt in ('ps', 'eps'):
            assert 'postscript' in el[:200]
        else:
            assert fmt in el[:200]


def test_base64_corner_cases():
    filepath = os.path.join(shared.IN_DIR, 'rectangle_10x10.jpg')
    with open(filepath, 'rb') as f:
        binary_data = f.read()
    base64_text = gv._internal.utils.web.binary_data_to_base64_text(binary_data)

    data_url = gv._internal.utils.web.base64_text_to_data_url(base64_text, data_format='jpg')
    assert data_url.startswith('data:image/jpeg;base64,')

    with pytest.raises(ValueError):
        gv._internal.utils.web.base64_text_to_data_url(base64_text, data_format='nonsense')


def test_exceptions():
    filepath = os.path.join(shared.IN_DIR, 'rectangle_10x10.jpg')

    # TypeError
    with pytest.raises(TypeError):
        gv.convert.image_to_html_element(42)
    with pytest.raises(TypeError):
        gv.convert.image_to_html_element(filepath, name=42)
    with pytest.raises(TypeError):
        gv.convert.image_to_html_element(filepath, width='hello')
    with pytest.raises(TypeError):
        gv.convert.image_to_html_element(filepath, height='hello')
    with pytest.raises(TypeError):
        gv.convert.image_to_html_element(filepath, unit=42)
    with pytest.raises(TypeError):
        gv.convert.image_to_html_element(filepath, data_format=42)

    # ValueError
    for fmt in ['nonsense', 'jp', 'svgg']:
        with pytest.raises(ValueError):
            gv.convert.image_to_html_element(filepath, data_format=fmt)

    # ValueError due to inexistent location
    with pytest.raises(ValueError):
        gv.convert.image_to_html_element('nonsense516%!$')

    # ValueError due to wrong URL
    with pytest.raises(ValueError):
        url = 'https://en.wikipedia.org/w/rest.php/v1/zwkenflkyuszesd'
        gv.convert.image_to_html_element(url)

    # ValueError due to undetectable format
    filepath = os.path.join(shared.IN_DIR, 'text_file')
    with pytest.raises(ValueError):
        gv.convert.image_to_html_element(filepath)
