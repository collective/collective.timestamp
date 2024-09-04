# -*- coding: utf-8 -*-

from collective.timestamp.interfaces import ITimeStamper
from collective.timestamp.utils import get_timestamp
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.interfaces import INamedField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from rfc3161ng import get_timestamp as get_timestamp_date
from zope.interface import implementer

import logging
import pytz

logger = logging.getLogger("collective.timestamp")


@implementer(ITimeStamper)
class TimeStamper(object):
    """Handle timestamping operations on an object"""

    def __init__(self, context):
        self.context = context

    def get_file_field(self):
        try:
            primary = IPrimaryFieldInfo(self.context, None)
            if (
                INamedField.providedBy(primary.field)
                and hasattr(primary.value, "getSize")
                and primary.value.getSize() > 0
            ):
                return primary
        except TypeError:
            pass

    def get_data(self):
        field = self.get_file_field()
        if field is None:
            logger.warning(
                f"Could not find the file field for {self.context.absolute_url()}"
            )
        return field.value.data

    def is_timestamped(self):
        return self.context.timestamp is not None

    def is_timestampable(self):
        return self.get_data() is not None and not self.is_timestamped()

    def timestamp(self):
        timestamp = get_timestamp(self.get_data())
        self.context.timestamp = NamedBlobFile(
            data=timestamp.prettyPrint(), filename="timestamp.tsr"
        )
        tzinfo = pytz.timezone("UTC")
        timestamp_date = get_timestamp_date(timestamp)
        self.context.setEffectiveDate(tzinfo.localize(timestamp_date))
        return get_timestamp(self.get_data())
