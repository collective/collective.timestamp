from collective.timestamp.interfaces import ITimeStamper


def modified_content(obj, event):
    handler = ITimeStamper(obj)
    if not handler.is_timestamped():
        # object is not timestamped, nothing to do here
        return
    # TODO check timestamp (again)
