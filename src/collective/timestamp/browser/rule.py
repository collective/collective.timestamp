from collective.timestamp.behaviors.timestamp import ITimestampableDocument
from collective.timestamp.utils import get_timestamp
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import NullAddForm
from plone.base.utils import pretty_title_or_id
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.namedfile.file import NamedBlobFile
from rfc3161ng import TimestampingError
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import logging

logger = logging.getLogger("collective.timestamp")


class ITimestampAction(Interface):
    """Interface for the configurable aspects of a timestamp action."""


@implementer(ITimestampAction, IRuleElementData)
class TimestampAction(SimpleItem):
    """The actual persistent implementation of the action element."""

    element = "collective.timestamp.actions.Timestamp"
    summary = _("Timestamp object")


@adapter(Interface, ITimestampAction, Interface)
@implementer(IExecutable)
class TimestampActionExecutor:
    """The executor for this action."""

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        if not obj:
            return False

        if not ITimestampableDocument.providedBy(self.context):
            return False
        elif self.context.timestamp is not None:
            return False
        elif self.context.timestampable_file is None:
            return False

        try:
            timestamp = get_timestamp(obj.timestampable_file.data)
        except TimestampingError as e:
            self.error(obj, str(e))
            logger.error(f"Timestamp rule failed for {obj.absolute_url()} : {str(e)}")
            return False

        obj.timestamp = NamedBlobFile(data=timestamp, filename="timestamp.tsr")
        logger.info(f"Timestamp generated for {obj.absolute_url()}")
        request = getattr(self.context, "REQUEST", None)
        if request is not None:
            title = pretty_title_or_id(obj, obj)
            message = _(
                "Timestamp file has been successfully generated and saved for ${name}",
                mapping={"name": title},
            )
            api.portal.show_message(message, request)
        return True

    def error(self, obj, error):
        request = getattr(self.context, "REQUEST", None)
        if request is not None:
            title = pretty_title_or_id(obj, obj)
            message = _(
                "Unable to timestamp ${name}: ${error}",
                mapping={"name": title, "error": error},
            )
            api.portal.show_message(message, request, type="error")


class TimestampAddForm(NullAddForm):
    """A degenerate "add form" for timestamp actions."""

    def create(self):
        return TimestampAction()
