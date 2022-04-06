__all__ = ["convert_line_endings"]

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'


def convert_line_endings(file_name: str):
    with open(file_name, "rb") as f:
        content = f.read()

    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

    with open(file_name, "wb") as f:
        f.write(content)
