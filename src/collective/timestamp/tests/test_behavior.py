# -*- coding: utf-8 -*-

from collective.timestamp.behaviors.timestamp import ITimestampableDocument
from collective.timestamp.testing import COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING
from plone import api
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.namedfile.file import NamedBlobFile
from Products.statusmessages.interfaces import IStatusMessage
from rfc3161ng import TimestampingError
from unittest.mock import patch
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import modified

import unittest


class TestBehavior(unittest.TestCase):

    layer = COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.document = api.content.create(
            container=self.portal,
            type="Document",
            id="my-document",
        )
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="my-file",
        )

    def test_behavior_interface(self):
        behavior = getUtility(IBehavior, "collective.timestamp")
        self.assertEqual(behavior.marker, ITimestampableDocument)
        self.assertTrue(ITimestampableDocument.providedBy(self.file))

    def test_action(self):
        view = getMultiAdapter((self.document, self.request), name="timestamp_utils")
        self.assertFalse(view.available())

        view = getMultiAdapter((self.file, self.request), name="timestamp_utils")
        self.assertFalse(view.available())
        self.file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        self.assertTrue(view.available())

        view.timestamp()
        messages = IStatusMessage(self.request)
        show = messages.show()
        self.assertEqual(len(show), 1)
        self.assertIn(
            "Timestamp file has been successfully generated and saved", show[0].message
        )

        self.file.timestamp = None
        with patch(
            "collective.timestamp.adapters.TimeStamper.timestamp",
            side_effect=TimestampingError,
        ):
            view.timestamp()
            messages = IStatusMessage(self.request)
            show = messages.show()
            self.assertEqual(len(show), 2)
            self.assertIn("Timestamp has failed", show[1].message)

    def test_subscribers(self):
        self.file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        modified(self.file, Attributes(IBasic, "IBasic.title"))
        messages = IStatusMessage(self.request)
        show = messages.show()
        self.assertEqual(len(show), 0)
        view = getMultiAdapter((self.file, self.request), name="timestamp_utils")
        self.assertTrue(view.available())
        view.timestamp()
        self.assertFalse(view.available())
        modified(self.file, Attributes(Interface, "file"))
        self.assertTrue(view.available())
        self.assertIsNone(self.file.timestamp)
        messages = IStatusMessage(self.request)
        show = messages.show()
        self.assertEqual(len(show), 2)
        self.assertIn(
            "Timestamp information has been removed since the data has changed",
            show[1].message,
        )
