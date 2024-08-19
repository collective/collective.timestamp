def modified_content(obj, event):
    if obj.timestamp is None:
        # object is not timestamped, nothing to do here
        return
    # TODO check timestamp (again)
