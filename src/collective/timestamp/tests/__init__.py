import unittest
from pathlib import Path
from unittest.mock import patch

from collective.timestamp.interfaces import ITimeStamper
from collective.timestamp.testing import COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING, \
    COLLECTIVE_TIMESTAMP_FUNCTIONAL_TESTING
from plone import api
from plone.namedfile import NamedBlobFile
from pyasn1.codec.der import decoder
from rfc3161ng import TimeStampResp
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TimestampBaseTestCase(unittest.TestCase):
    """Base test case for the collective.timestamp package."""

    def setUp(self):
        """Set up the test case."""
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
        self.timestamped_file = api.content.create(
            container=self.portal,
            type="File",
            id="timestamped-file",
        )
        self.timestamped_file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        mock_tsr_path = Path(__file__).parent / "resources/mock_tsr_file.tsr"
        with open(mock_tsr_path, "rb") as f:
            self.raw_tsr = f.read()
        self.tsr, _ = decoder.decode(self.raw_tsr, asn1Spec=TimeStampResp())
        with patch("rfc3161ng.api.RemoteTimestamper.__call__") as mock_timestamper:
            mock_timestamper.return_value = self.tsr
            handler = ITimeStamper(self.timestamped_file)
            handler.timestamp()
        logout()


class TimestampIntegrationTestCase(TimestampBaseTestCase):
    """Integration test case for the collective.timestamp package."""
    layer = COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]


class TimestampFunctionalTestCase(TimestampBaseTestCase):
    """Functional test case for the collective.timestamp package."""
    layer = COLLECTIVE_TIMESTAMP_FUNCTIONAL_TESTING

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
