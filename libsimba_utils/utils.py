from typing import List, Tuple, Union

from Crypto.Hash import keccak


def convert_to_bytes32_array(
    string: str, length: int, extract_single_array: bool = True
) -> Union[List, str]:
    byte_array = bytearray(32 * length)
    byte_val = bytearray(string, "utf8")
    byte_array[0 : len(byte_val)] = byte_val
    bytes32_arr = []
    for i in range(0, length):
        part = bytearray(32)
        part[:] = byte_array[32 * i : 32 + 32 * i]
        bytes32_arr.append("0x" + part.hex())
    if len(bytes32_arr) == 1 and extract_single_array:
        return bytes32_arr[0]
    return bytes32_arr


def convert_bytes32_to_string(
    bytes32_array: Union[List, Tuple, str], length: int = 1
) -> str:
    if isinstance(bytes32_array, (list, tuple)):
        byte_array = bytearray(32 * length)
        for i in range(0, length):
            chunk = bytearray.fromhex(bytes32_array[i][2:])
            byte_array[i * 32 :] = chunk
        bs = byte_array.decode("utf8")
        return bs.strip("\u0000")
    else:
        chunk = bytearray.fromhex(bytes32_array[2:])
        bs = chunk.decode("utf8")
        return bs.strip("\u0000")


def keccak_hash(value: str, bits: int = 256):
    return keccak.new(digest_bits=bits).update(value.encode("utf-8")).hexdigest()
