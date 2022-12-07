from functools import partial
from hashlib import md5

from typing import Iterable

import os


async def upload_helper(
    awaitable_create_method,
    awaitable_upload_method,
    path,
    source,
    source_type,
    chunk_size,
    **kwargs,
):
    file_size = os.path.getsize(source)

    await awaitable_create_method(
        path=path, source=source, source_type=source_type, size=file_size, **kwargs
    )

    for chunk_data in read_binary_chunks_from_file(
        file_name=source, chunk_size=chunk_size
    ):
        await awaitable_upload_method(path, **chunk_data)


def extract_kwargs(keys: Iterable, kwargs):
    return {key: kwargs.pop(key) for key in keys if key in kwargs}


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
                "Upload-Checksum": checksum,
            }
            yield {"headers": headers, "body": chunk}
            current_chunk_start += read_bytes
