"""pythonista.cloud is the package manager for Pythonista.

This module serves as the main interface.
"""
import sys

import _cloud
import _cloud.submitter


special_cases = {
    # Python stuff. I have no idea what these should actually be, but None
    # seems to work for now.
    "__spec__": None,
    "__path__": None,
}


class CloudImportHandler(object):
    """Handles all requests to the cloud module

    This includes:
    - from cloud import x
    - methods as part of the client API, such as update
    """
    def __getattr__(self, module_name):
        """Return a module object from the index

        There are some cases in which it is inappropriate to return a module
        for a requested name, including:
        - internally used module attributes like __path__
        - parts of the cloud API, like cloud.update

        If the requested name does not fit any of these cases, we search the
        index, download the module, and return it to the user.
        """
        # The module shouldn't be downloaded
        if module_name in special_cases:
            return special_cases[module_name]
        # The module is already installed
        elif module_name in sys.modules:
            return sys.modules[module_name]
        # The module is not installed.
        else:
            mod = _cloud.Module(module_name)
            mod.download()
            mod.install()
            return mod.importme()

    def __contains__(self, module_name):
        """Allows syntax of 'x in cloud' to check the index"""
        pass

    def update(self, module_name):
        """Re-download the latest version of a module."""
        if module_name not in sys.modules:
            raise AttributeError(("Module '{}' not installed, install via "
            "'from cloud import {}'").format(module_name, module_name))
        else:
            mod = _cloud.Module(module_name)
            mod.download()
            mod.install()
            return mod.importme()

    def config(self, **kwargs):
        """Used to require specific module versions."""
        raise NotImplementedError("Coming soon!")

    def submit(self, **kwargs):
        """Submit a package to the index."""
        _cloud.submitter.submit_module(kwargs)

if __name__ != "__main__":
    # This is being imported
    sys.modules[__name__] = CloudImportHandler()
else:
    # This is being run normally
    pass

