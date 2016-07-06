"""pythonista.cloud is the package manager for Pythonista.

This module serves as the main interface.
"""

import sys

import _cloud

special_cases = {
    # Python stuff. I have no idea what these should actually be, but None
    # seems to work for now.
    "__spec__": None,
    "__path__": None,
    # Other parts of pythonista.cloud
    "config": lambda: exec("raise NotImplementedError('Coming soon!')"),
    "update": lambda: exec("raise NotImplementedError('Coming soon!')")
}


class CloudImportHandler(object):
    """Implements custom behavior when running 'from cloud import x'"""
    def __getattr__(self, key):
        """ Add a module named 'key' from the index into your namespace.

        There are some cases in which it is inappropriate to return a module
        for a requested name, including:
        - internally used module attributes like __path__
        - parts of the cloud API, like cloud.update

        If the requested name does not fit any of these cases, we search the
        index, download the module, and return it to the user.
        """
        # The module shouldn't be downloaded
        if key in special_cases:
            return special_cases[key]
        # The module is already installed
        elif key in sys.modules:
            return sys.modules[key]
        # The module is not installed.
        else:
            mod = _cloud.Module(key)
            mod.download()
            mod.install()
            return mod.importme()

    def __contains__(self, key):
        """ Allows syntax of 'x in cloud' """
        pass


if __name__ != "__main__":
    # This is being imported
    sys.modules[__name__] = CloudImportHandler()
else:
    # This is being run normally
    pass
