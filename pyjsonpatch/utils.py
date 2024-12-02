def escape_json_ptr(ptr: str) -> str:
    """
    Escapes `/` and `~` to `~0` and `~1`, respectively.

    Based on RFC 9601 (https://datatracker.ietf.org/doc/html/rfc6901).
    
    :param ptr: The string to escape
    :return: The escaped result
    """
    if ptr.find("/") == -1 and ptr.find("~") == -1:
        return ptr
    return ptr.replace("~", "~0").replace("/", "~1")


def unescape_json_ptr(ptr: str) -> str:
    """
    Unescapes `~0` and `~1` to `/` and `~`, respectively.

    Based on RFC 9601 (https://datatracker.ietf.org/doc/html/rfc6901).

    :param ptr: The string to unescape
    :return: The unescaped result
    """
    return ptr.replace("~1", "/").replace("~0", "~")
