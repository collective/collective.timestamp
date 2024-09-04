# -*- coding: utf-8 -*-

from collective.timestamp import _
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from zope.interface import provider


@provider(IFormFieldProvider)
class ITimestampableDocument(model.Schema):
    """ """

    model.fieldset(
        "timestamp",
        label=_("Time stamp"),
        fields=["timestamp"],
    )

    read_permission(timestamp="collective.timestamp.read")
    write_permission(timestamp="collective.timestamp.write")
    timestamp = NamedBlobFile(
        title=_("Time Stamp Response (TSR) file"),
        required=False,
    )
