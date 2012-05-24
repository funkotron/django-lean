# -*- coding: utf-8 -*-
"""
    celery.datastructures
    ~~~~~~~~~~~~~~~~~~~~~

    Custom types and data structures.

    :copyright: (c) 2009 - 2011 by Ask Solem.
    :license: BSD, see LICENSE for more details.

"""
from __future__ import absolute_import
from __future__ import with_statement

import sys
import time
import traceback

from itertools import chain
from threading import RLock


class AttributeDictMixin(object):
    """Adds attribute access to mappings.

    `d.key -> d[key]`

    """

    def __getattr__(self, key):
        """`d.key -> d[key]`"""
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                    self.__class__.__name__, key))

    def __setattr__(self, key, value):
        """`d[key] = value -> d.key = value`"""
        self[key] = value


class AttributeDict(dict, AttributeDictMixin):
    """Dict subclass with attribute access."""
    pass


class DictAttribute(object):
    """Dict interface to attributes.

    `obj[k] -> obj.k`

    """

    def __init__(self, obj):
        self.obj = obj

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def setdefault(self, key, default):
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def __getitem__(self, key):
        try:
            return getattr(self.obj, key)
        except AttributeError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        setattr(self.obj, key, value)

    def __contains__(self, key):
        return hasattr(self.obj, key)

    def _iterate_items(self):
        return vars(self.obj).iteritems()
    iteritems = _iterate_items

    if sys.version_info >= (3, 0):
        items = _iterate_items
    else:

        def items(self):
            return list(self._iterate_items())


class ConfigurationView(AttributeDictMixin):
    """A view over an applications configuration dicts.

    If the key does not exist in ``changes``, the ``defaults`` dict
    is consulted.

    :param changes:  Dict containing changes to the configuration.
    :param defaults: Dict containing the default configuration.

    """
    changes = None
    defaults = None
    _order = None

    def __init__(self, changes, defaults):
        self.__dict__.update(changes=changes, defaults=defaults,
                             _order=[changes] + defaults)

    def __getitem__(self, key):
        for d in self._order:
            try:
                return d[key]
            except KeyError:
                pass
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.changes[key] = value

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def setdefault(self, key, default):
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def update(self, *args, **kwargs):
        return self.changes.update(*args, **kwargs)

    def __contains__(self, key):
        for d in self._order:
            if key in d:
                return True
        return False

    def __repr__(self):
        return repr(dict(self.iteritems()))

    def __iter__(self):
        return self.iterkeys()

    def _iter(self, op):
        # defaults must be first in the stream, so values in
        # changes takes precedence.
        return chain(*[op(d) for d in reversed(self._order)])

    def _iterate_keys(self):
        return self._iter(lambda d: d.iterkeys())
    iterkeys = _iterate_keys

    def _iterate_items(self):
        return self._iter(lambda d: d.iteritems())
    iteritems = _iterate_items

    def _iterate_values(self):
        return self._iter(lambda d: d.itervalues())
    itervalues = _iterate_values

    def keys(self):
        return list(self._iterate_keys())

    def items(self):
        return list(self._iterate_items())

    def values(self):
        return list(self._iterate_values())
