from collective.timestamp.interfaces import ITimestampingSettings
from plone import api
from pyasn1.codec.der import decoder
from pyasn1.codec.der import encoder
from rfc3161ng import get_timestamp as get_timestamp_date
from rfc3161ng import RemoteTimestamper
from rfc3161ng import TimeStampResp

import pytz


def localize_utc_date(date):
    tzinfo = pytz.timezone("UTC")
    return tzinfo.localize(date)


def get_timestamp(file_content):
    service_url = api.portal.get_registry_record(
        "timestamping_service_url",
        interface=ITimestampingSettings,
    )
    timestamper = RemoteTimestamper(
        service_url,
        certificate=b"",
        hashname="sha256",
    )
    tsr = timestamper(
        data=file_content,
        include_tsa_certificate=True,
        return_tsr=True,
    )
    timestamp_token = tsr.time_stamp_token
    timestamp_date = get_timestamp_date(timestamp_token)
    return {
        "tsr": encoder.encode(tsr),
        "timestamp_date": localize_utc_date(timestamp_date),
    }


def get_timestamp_date_from_tsr(tsr_data):
    tsr, _ = decoder.decode(tsr_data, asn1Spec=TimeStampResp())
    timestamp_token = tsr.time_stamp_token
    timestamp_date = get_timestamp_date(timestamp_token)
    return localize_utc_date(timestamp_date)
