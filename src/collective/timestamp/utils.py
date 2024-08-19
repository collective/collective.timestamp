from collective.timestamp.browser.controlpanel import ITimestampingSettings
from plone import api
from pyasn1.codec.der.decoder import decode
from rfc3161ng import RemoteTimestamper
from rfc3161ng import TimeStampToken


def get_timestamp(file_content):
    service_url = api.portal.get_registry_record(
        "timestamping_service_url", interface=ITimestampingSettings
    )
    timestamper = RemoteTimestamper(service_url, certificate=b"", hashname="sha256")
    value = timestamper(data=file_content, include_tsa_certificate=True)
    tst, substrate = decode(value, asn1Spec=TimeStampToken())
    return tst.prettyPrint()
