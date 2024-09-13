# -*- coding: utf-8 -*-

from collective.timestamp import logger
from collective.timestamp.interfaces import ITimeStamper
from collective.timestamp.utils import get_timestamp
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.interfaces import INamedField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IAttributes


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
            return
        return field.value.data

    def file_has_changed(self, obj, event):
        field = self.get_file_field()
        fieldname = field.fieldname
        for d in event.descriptions:
            if not IAttributes.providedBy(d):
                continue
            if fieldname in d.attributes:
                return True
        return False

    def is_timestamped(self):
        return self.context.timestamp is not None

    def is_timestampable(self):
        if not self.context.enable_timestamping:
            return False
        elif self.is_timestamped():
            return False
        return self.get_data() is not None

    def timestamp(self):
        if not self.is_timestampable():
            raise ValueError("This content is not timestampable")
        timestamp = get_timestamp(self.get_data())
        self.context.timestamp = NamedBlobFile(
            data=timestamp["tsr"], filename="timestamp.tsr"
        )
        self.context.setEffectiveDate(timestamp["timestamp_date"])
        self.context.reindexObject(
            idxs=["effective", "effectiveRange", "is_timestamped"]
        )
