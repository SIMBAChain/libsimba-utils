import unittest
from libsimba_utils.utils import convert_bytes32_to_string, convert_to_bytes32_array


class TestSer(unittest.TestCase):

    def test_bytes_to_string(self):
        edition_bytes = convert_to_bytes32_array(" Edition 1000000000/1000000000", 1)
        edition_str = convert_bytes32_to_string(edition_bytes, 1)
        assert edition_str == " Edition 1000000000/1000000000"

        data = {
            "name": "2020 Lorem ipsum dolor sit amet",
            "contentHash": "0x8eebc511ae55f498d9f0a3a1ddcb58a0bb639c9f8f89d6c83e430f25de900ff2",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut lab",
            "image": "https://picsum.photos/200/300/?t=asdfj938j0qf98jas0df8je098j2faa",
        }
        inputs = {
            "name": convert_to_bytes32_array(data["name"], 1),
            "description": convert_to_bytes32_array(data["description"], 4),
            "image": convert_to_bytes32_array(data["image"], 4),
            "contentHash": data["contentHash"]
        }

        outputs = {
            "name": convert_bytes32_to_string(inputs["name"], 1),
            "description": convert_bytes32_to_string(inputs["description"], 4),
            "image": convert_bytes32_to_string(inputs["image"], 4),
            "contentHash": inputs["contentHash"]
        }
        assert data == outputs
