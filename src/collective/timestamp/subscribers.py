# -*- coding: utf-8 -*-

from collective.timestamp import _
from collective.timestamp.interfaces import ITimeStamper
from plone import api
from zope.lifecycleevent.interfaces import IAttributes


def modified_content(obj, event):
    handler = ITimeStamper(obj)
    if not handler.is_timestamped():
        # object is not timestamped, nothing to do here
        return
    timestamped_field = handler.get_file_field()
    fieldname = timestamped_field.fieldname
    for d in event.descriptions:
        if not IAttributes.providedBy(d):
            # we do not have fields change description, but maybe a request
            continue
        if fieldname in d.attributes:
            # primary file field has changed, we need to remove timestamp
            obj.timestamp = None
            obj.reindexObject(idxs=["is_timestamped"])
            request = getattr(obj, "REQUEST", None)
            if request is not None:
                message = _(
                    "Timestamp information has been removed since the file has changed"
                )
                api.portal.show_message(message, request)
