# -*- coding: utf-8 -*-

from collective.timestamp.behaviors.timestamp import ITimestampableDocument
from plone.indexer import indexer


@indexer(ITimestampableDocument)
def is_timestamped(obj):
    return obj.timestamp is not None
