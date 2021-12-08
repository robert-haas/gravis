"""Rendering the HTML visualization to get static images."""

import os
import time

from ..utils.args import check_arg


def render_and_capture(html_text, data_format='png', webdriver='chrome',
                       capture_delay=1.0, start_delay=0.1, stop_delay_fast=0.25,
                       stop_delay_slow=10.0):
    """Open a HTML visualization with Selenium and export the drawing area as SVG, PNG or JPG."""
    import http.server
    import random
    import tempfile
    import threading

    # Argument processing
    check_arg(html_text, 'html_text', str)
    check_arg(data_format, 'data_format', str, ['png', 'jpg', 'svg'])
    check_arg(webdriver, 'webdriver', str, ['chrome', 'firefox'])
    check_arg(capture_delay, 'capture_delay', (int, float))
    check_arg(start_delay, 'start_delay', (int, float))
    check_arg(stop_delay_fast, 'stop_delay_fast', (int, float))
    check_arg(stop_delay_slow, 'stop_delay_slow', (int, float))
    create_driver = create_chrome_driver if webdriver == 'chrome' else create_firefox_driver

    # Functions
    def open_browser_and_stop_server(results):
        with tempfile.TemporaryDirectory() as tmpdir:
            driver = create_driver(tmpdir)
            driver.get(url)
            time.sleep(capture_delay)
            image = capture_image_by_click(data_format, driver, tmpdir)
            results.append(image)
            driver.close()
        # Start thread 2: Stop the server slowly, even if no GET request is ever received
        timer_stop_slow.start()

    def stop_all():
        # Stop server
        server.shutdown()
        # Stop all timer threads
        timer_stop_slow.cancel()
        timer_stop_fast.cancel()

    class MyHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            """Serve the given HTML text to a GET request from the webbrowser."""
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(html_text, 'utf-8'))
            # Start thread 3: Stop the server quickly after the first GET request was received
            if not timer_stop_fast.is_alive():
                timer_stop_fast.start()

        def log_message(self, format, *args):
            """Show no log messages."""

    local_host = '127.0.0.1'
    for _ in range(13):
        try:
            random_port = random.randint(49152, 65535)  # port range used for "temporary purposes"
            server_address = (local_host, random_port)
            server = http.server.HTTPServer(server_address, MyHandler)
            url = 'http://{}:{}'.format(local_host, random_port)
            break
        except Exception:
            pass
    else:
        message = (
            'Could not start a local webserver for serving HTML text to a webbrowser. '
            'No free port could be found.')
        raise OSError(message)

    # Define threads 1 to 3
    results = []
    timer_run = threading.Timer(start_delay, open_browser_and_stop_server, args=(results,))
    timer_stop_slow = threading.Timer(stop_delay_slow, stop_all)
    timer_stop_fast = threading.Timer(stop_delay_fast, stop_all)

    # Start thread 1: Open webbrowser with some delay, stop the server with some delay
    timer_run.start()

    # Go into server loop
    server.serve_forever()

    timer_run.join()
    try:
        image = results[0]
        assert image is not None
    except Exception:
        msg = (
            'An error occurred while rendering the HTML text with Selenium and '
            'trying to capture an image in {} format. This can have various reasons '
            'that are not easy to detect and report, sorry!'.format(data_format))
        raise ValueError(msg)
    return image


def create_chrome_driver(directory, headless=True):
    """Create a Chrome driver instance suitable for downloading files and headless by default."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # Automatically download images to a chosen directory
    options = Options()
    options.add_experimental_option('prefs', {
        'download.default_directory': directory,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True})

    # Headless: Work without opening a browser window
    if headless:
        options.add_argument('--headless')

    # Driver
    driver = webdriver.Chrome(options=options)
    return driver


def create_firefox_driver(directory, headless=True):
    """Create a Firefox driver instance suitable for downloading files and headless by default."""
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service

    # Create no geckodriver.log file in working directory
    service = Service(log_path=os.devnull)

    # Automatically download images to a chosen directory
    mime_types = 'image/png,image/jpeg,image/svg+xml'
    options = Options()
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.manager.showWhenStarting', False)
    options.set_preference('browser.download.dir', directory)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', mime_types)
    options.set_preference("browser.download.viewableInternally.enabledTypes", "")  # dirty hack

    # Headless: Work without opening a browser window
    if headless:
        options.headless = True

    # Driver
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def capture_image_by_click(data_format, driver, directory):
    """Capture an image of the rendered graph visualization by clicking an export button."""
    data = None

    # Toggle menu
    menu_button = driver.find_element('css selector', '[id$=-menu-toggle-button]')
    menu_button.click()

    # JPG, PNG or SVG button
    img_button = driver.find_element('css selector', '[id$=-{}]'.format(data_format))
    img_button.click()
    filename = 'graph.{}'.format(data_format)
    filepath = os.path.join(directory, filename)
    read_mode = 'r' if data_format == 'svg' else 'rb'
    for i in range(20):
        time.sleep(0.25)
        try:
            with open(filepath, read_mode) as file_handle:
                data = file_handle.read()
            break
        except FileNotFoundError:
            pass
    return data
