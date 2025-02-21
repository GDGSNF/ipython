""" Utilities for accessing the platform's clipboard.
"""

import subprocess

from IPython.core.error import TryNext
import IPython.utils.py3compat as py3compat


class ClipboardEmpty(ValueError):
    pass


def win32_clipboard_get():
    """Get the current clipboard's text on Windows.

    Requires Mark Hammond's pywin32 extensions.
    """
    try:
        import win32clipboard
    except ImportError as e:
        raise TryNext(
            "Getting text from the clipboard requires the pywin32 "
            "extensions: http://sourceforge.net/projects/pywin32/"
        ) from e
    win32clipboard.OpenClipboard()
    try:
        text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    except (TypeError, win32clipboard.error):
        try:
            text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            text = py3compat.cast_unicode(text, py3compat.DEFAULT_ENCODING)
        except (TypeError, win32clipboard.error) as e:
            raise ClipboardEmpty from e
    finally:
        win32clipboard.CloseClipboard()
    return text


def osx_clipboard_get() -> str:
    """Get the clipboard's text on OS X."""
    p = subprocess.Popen(["pbpaste", "-Prefer", "ascii"], stdout=subprocess.PIPE)
    bytes_, stderr = p.communicate()
    # Text comes in with old Mac \r line endings. Change them to \n.
    bytes_ = bytes_.replace(b"\r", b"\n")
    return py3compat.decode(bytes_)


def tkinter_clipboard_get():
    """Get the clipboard's text using Tkinter.

    This is the default on systems that are not Windows or OS X. It may
    interfere with other UI toolkits and should be replaced with an
    implementation that uses that toolkit.
    """
    try:
        from tkinter import Tk, TclError
    except ImportError as e:
        raise TryNext(
            "Getting text from the clipboard on this platform requires tkinter."
        ) from e

    root = Tk()
    root.withdraw()
    try:
        text = root.clipboard_get()
    except TclError as e:
        raise ClipboardEmpty from e
    finally:
        root.destroy()
    text = py3compat.cast_unicode(text, py3compat.DEFAULT_ENCODING)
    return text
