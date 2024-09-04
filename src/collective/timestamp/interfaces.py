# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.timestamp import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveTimestampLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ITimeStamper(Interface):
    """"""


class ITimestampingSettings(Interface):

    timestamping_service_url = schema.URI(
        title=_("URL of the timestamping service you want to use"),
        default="http://freetsa.org/tsr",
        required=False,
    )
