"""
Wrappers for :mod:`sklearn`.


This module loads corresponding modules in ``sklearn`` by demand, just
as ``sklearn`` does. Its contents depend on those of the ``sklearn``
in your system when it is loaded.

Example:

    >>> import sklearn
    >>> import ibex

    :mod:`sklearn.linear_model` is part of ``sklearn``,
    therefore :mod:`ibex.sklearn` will have a counterpart.

    >>> 'linear_model' in sklearn.__all__
    True
    >>> 'linear_model' in ibex.sklearn.__all__
    True
    >>> from ibex.sklearn import linear_model # doctest: +SKIP

    ``foo`` is not part of ``sklearn``,
    therefore :mod:`ibex.sklearn` will not have a counterpart.

    >>> 'foo' in sklearn.__all__
    False
    >>> 'foo' in ibex.sklearn.__all__
    False
    >>> try:
    ...     from ibex.sklearn import foo
    ... except ImportError:
    ...     print('caught')
    caught

"""


from __future__ import absolute_import


import sys
import imp
import string

import six
import sklearn

from ._model_selection import update_module as _model_selection_update_module
from ._pipeline import update_module as _pipeline_update_module
from ._preprocessing import update_module as _preprocessing_update_module


__all__ = sklearn.__all__


_code = string.Template('''
"""
Auto-generated :mod:`ibex.sklearn` wrapper for :mod:`sklearn.$mod_name`.
"""


from __future__ import absolute_import


import inspect

from sklearn import $mod_name as _orig
from sklearn import base

import ibex


for name in dir(_orig):
    if name.startswith('_'):
        continue
    est = getattr(_orig, name)
    try:
        if inspect.isclass(est) and issubclass(est, base.BaseEstimator):
            globals()[name] = ibex.frame(est)
        else:
            globals()[name] = est
    except TypeError as e:
        pass''')


class _NewModuleLoader(object):
    """
    Load the requested module via standard import, or create a new module if
    not exist.
    """

    def load_module(self, full_name):
        orig = full_name.split('.')[-1]

        mod = sys.modules.setdefault(full_name, imp.new_module(full_name))
        mod.__file__ = ''
        mod.__name__ = full_name
        mod.__path__ = ''
        mod.__loader__ = self
        mod.__package__ = '.'.join(full_name.split('.')[:-1])

        code = _code.substitute({'mod_name': orig})

        six.exec_(code, mod.__dict__)

        _model_selection_update_module(orig, mod)
        _pipeline_update_module(orig, mod)
        _preprocessing_update_module(orig, mod)

        return mod


class _ModuleFinder(object):
    def install(self):
        sys.meta_path[:] = [x for x in sys.meta_path if self != x] + [self]

    def find_module(self, full_name, _=None):
        if not full_name.startswith('ibex.sklearn.'):
            return

        if full_name.split('.')[-1].startswith('_'):
            return

        return _NewModuleLoader()


loader = _ModuleFinder()
loader.install()

