# -*- coding: utf-8 -*-
from collective.timestamp.behaviors.timestamp import ITimestampableDocument
from collective.timestamp.testing import COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class TestBehavior(unittest.TestCase):

    layer = COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_timestamp(self):
        behavior = getUtility(IBehavior, "collective.timestamp")
        self.assertEqual(behavior.marker, ITimestampableDocument)
