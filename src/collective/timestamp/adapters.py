# -*- coding: utf-8 -*-

from collective.timestamp.interfaces import ITimeStamper
from collective.timestamp.utils import get_timestamp
from plone.namedfile.interfaces import INamedField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.interface import implementer

import logging

logger = logging.getLogger("collective.timestamp")


@implementer(ITimeStamper)
class TimeStamper(object):
    """Handle timestamping operations on an object"""

    def __init__(self, context):
        self.context = context

    def get_data(self):
        try:
            primary = IPrimaryFieldInfo(self.context, None)
            if (
                INamedField.providedBy(primary.field)
                and hasattr(primary.value, "getSize")
                and primary.value.getSize() > 0
            ):
                return primary.value.data
        except TypeError:
            pass
        logger.warning(
            f"Could not find the file field for {self.context.absolute_url()}"
        )

    def is_timestamped(self):
        return self.context.timestamp is not None

    def is_timestampable(self):
        return self.get_data() is not None and not self.is_timestamped()

    def timestamp(self):
        return get_timestamp(self.get_data())
