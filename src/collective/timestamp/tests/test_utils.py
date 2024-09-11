# -*- coding: utf-8 -*-

from collective.timestamp.testing import COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING
from collective.timestamp.utils import get_timestamp
from collective.timestamp.utils import get_timestamp_date_from_tsr
from collective.timestamp.utils import localize_utc_date
from datetime import datetime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile

import unittest
import pytz


class TestUtils(unittest.TestCase):

    layer = COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="my-file",
        )

    def test_localize_utc_date(self):
        naive_datetime = datetime(2024, 9, 10, 12, 0, 0)
        localized_datetime = localize_utc_date(naive_datetime)
        expected_datetime = datetime(2024, 9, 10, 12, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(localized_datetime, expected_datetime)

    def test_get_timestamp(self):
        self.file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        result = get_timestamp(self.file.file.data)
        self.assertTrue("tsr" in result)
        self.assertTrue("timestamp_date" in result)

    def test_get_timestamp_date_from_tsr(self):
        self.file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        result = get_timestamp(self.file.file.data)
        verif_date = get_timestamp_date_from_tsr(result["tsr"])
        self.assertEqual(result["timestamp_date"], verif_date)
