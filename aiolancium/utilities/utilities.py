from functools import partial
from hashlib import md5


def get_method_name(arg):
    while isinstance(arg, partial):
        arg = arg.args[0]
    return arg


def read_binary_chunks_from_file(file_name, chunk_size):
    with open(file_name, "rb") as f:
        current_chunk_start = 0
        for chunk in iter(partial(f.read, chunk_size), b""):
            read_bytes = len(chunk)
            checksum = md5(chunk).hexdigest()
            headers = {
                "Content-Length": str(read_bytes),
                "Upload-Offset": str(current_chunk_start),
                "Upload-Checksun": checksum,
            }
            yield {"headers": headers, "body": chunk}
            current_chunk_start += read_bytes
