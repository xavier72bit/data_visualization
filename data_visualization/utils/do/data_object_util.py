import uuid


def general_primary_key():
    """
    返回一个字符串格式的UUID
    """
    return str(uuid.uuid4())