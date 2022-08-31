import unittest
import pytest
from libsimba_utils.wallet import Wallet
from libsimba_utils.exceptions import (
    SimbaMnemonicException,
    SimbaWalletNotFoundException,
    SimbaPrivateKeyException,
    SimbaTransactionException
)


class TestWallet(unittest.TestCase):
    def test_generate_from_mnemonic(self):
        wallet = Wallet()
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        wallet.generate_from_mnemonic(mnemonic)
        self.assertIsNotNone(wallet.wallet)
        self.assertEqual(wallet.wallet.mnemonic(), mnemonic)

    def test_generate_from_mnemonic_invalid(self):
        wallet = Wallet()
        mnemonic = "invalid"
        with pytest.raises(SimbaMnemonicException) as exc:
            wallet.generate_from_mnemonic(mnemonic)
        self.assertIn("Invalid mnemonic words", str(exc))
        self.assertIsNone(wallet.wallet)

    def test_generate_from_mnemonic_no_param(self):
        wallet = Wallet()
        wallet.generate_from_mnemonic()
        self.assertIsNotNone(wallet.wallet.mnemonic())

    def test_generate_from_private_key(self):
        wallet = Wallet()
        private_key = "1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67"
        wallet.generate_from_private_key(private_key)
        self.assertIsNotNone(wallet.wallet)
        self.assertEqual(wallet.wallet.private_key(), private_key)

    def test_generate_from_private_key_invalid(self):
        wallet = Wallet()
        private_key = "invalid"
        with pytest.raises(SimbaPrivateKeyException) as exc:
            wallet.generate_from_private_key(private_key)
        self.assertIn("Invalid private key", str(exc))
        self.assertIsNone(wallet.wallet)

    def test_delete_wallet(self):
        wallet = Wallet()
        wallet.wallet = "bob"
        wallet.delete_wallet()
        self.assertIsNone(wallet.wallet)

    def test_delete_no_wallet(self):
        wallet = Wallet()
        wallet.delete_wallet()
        self.assertIsNone(wallet.wallet)

    def test_wallet_exists_true(self):
        wallet = Wallet()
        wallet.wallet = "bob"
        self.assertTrue(wallet.wallet_exists())

    def test_wallet_exists_false(self):
        wallet = Wallet()
        self.assertFalse(wallet.wallet_exists())

    def test_wallet_sign_transaction(self):
        wallet = Wallet()
        private_key = "1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67"
        wallet.generate_from_private_key(private_key)
        transaction_payload = {
            "to": "0xdea35e452b7367c43330e0065ec22538f545333b",
            "value": 0,
            "gas": "0x5d6a",
            "gasPrice": "0x3b9aca00",
            "data": "0xdb7eff7c00000000",
            "nonce": "0x2",
        }
        signature = wallet.sign_transaction(transaction_payload)

        expected_sig = {
            'rawTransaction': '0xf86b02843b9aca00825d6a94dea35e452b7367c43330e0065ec22538f545333b8088db7eff7c000000001ba0b4985b74787ac27bb1bde40adc97dabdb97a38623dd6150e8ec3b3fa5581e95aa00809c0633c1d03db77f7fbaf357da964c93d9d4a6f041b0aa92d83bb9481ab9a',
            'hash': '0x5458728331d56f0b1279fc050f0f4488fef6f8c19ab19a95c2676f33545a73d9',
            'r': 81685504697793611067721356979325529201491251746049320434783832819291893393754,
            's': 3635732222913114008708416452560996557652025348427230851023132220765216287642,
            'v': 27,
        }
        self.assertEqual(signature, expected_sig)

    def test_wallet_sign_transaction_no_wallet(self):
        wallet = Wallet()
        with pytest.raises(SimbaWalletNotFoundException) as exc:
            wallet.sign_transaction({})
        self.assertIn("No wallet loaded!", str(exc))

    def test_wallet_sign_transaction_invalid_addr(self):
        wallet = Wallet()
        private_key = "1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67"
        wallet.generate_from_private_key(private_key)
        transaction_payload = {
            "to": "0xdea35e452b",
            "value": 0,
            "gas": "0x5d6a",
            "gasPrice": "0x3b9aca00",
            "data": "0xdb7eff7c00000000",
            "nonce": "0x2",
        }
        with pytest.raises(SimbaTransactionException) as exc:
            wallet.sign_transaction(transaction_payload)
        self.assertIn("Transaction had invalid fields", str(exc))

    def test_wallet_sign_transaction_missing_key(self):
        wallet = Wallet()
        private_key = "1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67"
        wallet.generate_from_private_key(private_key)
        transaction_payload = {
            "value": 0,
            "gas": "0x5d6a",
            "gasPrice": "0x3b9aca00",
            "data": "0xdb7eff7c00000000",
            "nonce": "0x2",
        }
        with pytest.raises(SimbaTransactionException) as exc:
            wallet.sign_transaction(transaction_payload)
        self.assertIn("Missing field in transaction: 'to'", str(exc))

    def test_get_address(self):
        wallet = Wallet()
        private_key = "1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67"
        wallet.generate_from_private_key(private_key)
        addr = wallet.get_address()
        self.assertEqual(addr, "0xa8E070649A1D98651D281FdD428BD3EeC0d279e0")

    def test_wallet_get_address_no_wallet(self):
        wallet = Wallet()
        with pytest.raises(SimbaWalletNotFoundException) as exc:
            wallet.get_address()
        self.assertIn("No wallet loaded!", str(exc))
