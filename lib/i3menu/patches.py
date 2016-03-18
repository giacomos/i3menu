# -*- coding: utf-8 -*-
from zope.schema import vocabulary


def monkeypatch_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


@monkeypatch_method(vocabulary)
def _createTermTree(ttree, dict_):
    for key in dict_.keys():
        term = vocabulary.SimpleTerm(key[1], key[0], key[-1])
        ttree[term] = vocabulary.TreeVocabulary.terms_factory()
        _createTermTree(ttree[term], dict_[key])
    return ttree
