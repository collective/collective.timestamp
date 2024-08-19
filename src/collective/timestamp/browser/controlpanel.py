# -*- coding: utf-8 -*-

from collective.timestamp import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ITimestampingSettings(Interface):

    timestamping_service_url = schema.URI(
        title=_("URL of the timestamping service you want to use"),
        default="http://freetsa.org/tsr",
        required=False,
    )


class TimestampingControlPanelForm(RegistryEditForm):
    label = _("Timestamping settings")
    schema = ITimestampingSettings


TimestampingControlPanelView = layout.wrap_form(
    TimestampingControlPanelForm, ControlPanelFormWrapper
)
