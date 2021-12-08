"""Centralized access to operating system functionality."""

import errno as _errno
import os as _os


def is_file(filepath, raise_exception=False):
    """Check if a file exists.

    Parameters
    ----------
    filepath : str
    raise_exception : bool

    Returns
    -------
    file_exists : bool

    Raises
    ------
    FileExistsError
        If there already is a file at the given filepath and raise_exception is True.

    """
    file_exists = _os.path.isfile(filepath)
    if raise_exception and file_exists:
        raise FileExistsError(_errno.EEXIST, _os.strerror(_errno.EEXIST), filepath)
    return file_exists


def is_nonempty_file(filepath, raise_exception=False):
    """Check if a file exists and is non-empty.

    Parameters
    ----------
    filepath : str
    raise_exception : bool

    Returns
    -------
    nonempty_file_exists : bool

    Raises
    ------
    FileExistsError
        If there already is a nonempty file at the given filepath and raise_exception is True.

    """
    nonempty_file_exists = _os.path.isfile(filepath) and _os.path.getsize(filepath) > 0
    if raise_exception and nonempty_file_exists:
        raise FileExistsError(_errno.EEXIST, _os.strerror(_errno.EEXIST), filepath)
    return nonempty_file_exists


def open_in_webbrowser(html_text, start_delay=0.1, stop_delay_fast=0.25, stop_delay_slow=10.0):
    """Open the given HTML text in the default webbrowser.

    A short-lived local HTTP server is created that serves HTML text, so that
    it can be opened in the default webbrowser. An alternative would be to write
    the HTML text to a temporary file and open this file in the webbrowser.

    Parameters
    ----------
    html_text : str
    start_delay : float
        Delay between starting the server and opening the webbrowser in another thread.
        If too short, the webbrowser might send the request before the server is running.
    stop_delay_fast : float
        Delay between opening the webbrowser (or a new tab) and shutting down the server
        after it received the first GET request from the browser.
    stop_delay_slow : float
        Delay between opening the webbrowser (or a new tab) and shutting down the server
        even if it never receives a GET request, e.g. because the browser does not open.

    References
    ----------
    - https://stackoverflow.com/questions/19040055/how-do-i-shutdown-an-httpserver-from-inside-a-request-handler-in-python
    - https://stackoverflow.com/questions/3389305/how-to-silent-quiet-httpserver-and-basichttprequesthandlers-stderr-output
    - https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Note

    """
    import http.server
    import random
    import threading
    import webbrowser

    def open_browser_and_stop_server():
        # Open webbrowser
        webbrowser.open(url)
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
    timer_run = threading.Timer(start_delay, open_browser_and_stop_server)
    timer_stop_slow = threading.Timer(stop_delay_slow, stop_all)
    timer_stop_fast = threading.Timer(stop_delay_fast, stop_all)

    # Start thread 1: Open webbrowser with some delay, stop the server with some delay
    timer_run.start()

    # Go into server loop
    server.serve_forever()
