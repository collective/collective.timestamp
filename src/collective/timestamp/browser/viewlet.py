# -*- coding: utf-8 -*-

from collective.timestamp.interfaces import ITimeStamper
from plone.app.layout.viewlets import common


class TimestampViewlet(common.ViewletBase):

    def available(self):
        handler = ITimeStamper(self.context)
        return handler.is_timestamped()
