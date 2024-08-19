# -*- coding: utf-8 -*-

from collective.timestamp import _
from collective.timestamp.behaviors.timestamp import ITimestampableDocument
from collective.timestamp.utils import get_timestamp
from plone import api
from plone.namedfile.file import NamedBlobFile
from Products.Five.browser import BrowserView
from rfc3161ng import TimestampingError

import logging

logger = logging.getLogger("collective.timestamp")


class TimestampView(BrowserView):

    def available(self):
        """
        Show timestamp action only if content is stampable and not already
        stamped.
        """
        if not ITimestampableDocument.providedBy(self.context):
            return False
        elif self.context.timestamp is not None:
            return False
        elif self.context.timestampable_file is None:
            return False
        return True

    def timestamp(self):
        obj = self.context
        try:
            timestamp = get_timestamp(obj.timestampable_file.data)
        except TimestampingError as e:
            api.portal.show_message(
                _("Timestamp has failed."),
                self.request,
                type="error",
            )
            logger.error(f"Timestamp action failed for {obj.absolute_url()} : {str(e)}")
            self.request.response.redirect(f"{self.context.absolute_url()}/view")
            return

        obj.timestamp = NamedBlobFile(data=timestamp, filename="timestamp.tsr")
        logger.info(f"Timestamp generated for {obj.absolute_url()}")
        api.portal.show_message(
            _("Timestamp file has been successfully generated and saved"), self.request
        )
        # TODO check redirect file view
        self.request.response.redirect(f"{self.context.absolute_url()}/view")
