from typing import List, Tuple, Union

from Crypto.Hash import keccak


def convert_to_bytes32_array(
    string: str, length: int, extract_single_array: bool = False, prefix: bool = True
) -> Union[List, str]:
    """
    Convert a string to an aray of byte32 arrays in hex representation.
    The string will be truncated if it does not fit into the arrays (32 bytes * length)
    :param string: the string to convert
    :param length: the length of the array to return.
    :param extract_single_array: If a single length array, whether to return just the bytes, i.e.,
           a single byte32 array.
    :param prefix: whether or not to prefix the hex strings with '0x'.
    :return: Either an array of byte arrays or a single byte array.
    """
    byte_array = bytearray(32 * length)
    byte_val = bytearray(string, "utf8")
    byte_array[0 : len(byte_val)] = byte_val
    bytes32_arr = []
    for i in range(0, length):
        part = bytearray(32)
        part[:] = byte_array[32 * i : 32 + 32 * i]
        pref = "0x" if prefix else ""
        bytes32_arr.append(f"{pref}{part.hex()}")
    if len(bytes32_arr) == 1 and extract_single_array:
        return bytes32_arr[0]
    return bytes32_arr


def convert_bytes32_to_string(
    bytes32_array: Union[List, Tuple, str], length: int = None
) -> str:
    """
    Convert a bytes32 in hex representation or an array of
    bytes32 in hex representation to a string.
    The representations are assumed to
    :param bytes32_array: the array of bytes or byte arrays
    :param length: The length of the array to convert if input is an array.
           If none, defaults to the length of the input array.
    :return: a string
    """
    if isinstance(bytes32_array, (list, tuple)):
        if length is None:
            length = len(bytes32_array)
        byte_array = bytearray(32 * length)
        for i in range(0, length):
            offset = 2 if bytes32_array[i].startswith("0x") else 0
            chunk = bytearray.fromhex(bytes32_array[i][offset:])
            byte_array[i * 32 :] = chunk
        bs = byte_array.decode("utf8")
    else:
        offset = 2 if bytes32_array.startswith("0x") else 0
        chunk = bytearray.fromhex(bytes32_array[offset:])
        bs = chunk.decode("utf8")
    return bs.strip("\u0000")


def keccak_hash(value: str, bits: int = 256, as_hex: bool = True) -> Union[str, bytes]:
    """
    HAsh a value.
    :param value: the value to hash
    :param bits: the numver of bits - default is 256
    :param as_hex: whether to return a hex digest or the raw bytes
    :return:
    """
    k_hash = keccak.new(digest_bits=bits).update(value.encode("utf-8"))
    if as_hex:
        return k_hash.hexdigest()
    else:
        return k_hash.digest()


def string_to_uint256(value: str, big_endian: bool = True) -> int:
    """
    Convert any length string to an unsigned 256 bit integer via hashing
    :param value: The string value to convert
    :param big_endian: whether to use big or little endian byte order. Solidity keccak uses big.
    :return: an integer
    """
    hash_val = keccak_hash(value, as_hex=False)
    return (
        int.from_bytes(hash_val, byteorder="big", signed=False)
        if big_endian
        else (int.from_bytes(hash_val, byteorder="little", signed=False))
    )
