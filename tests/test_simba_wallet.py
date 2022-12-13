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
            "chainId": "0x1",
            "to": "0xdea35e452b7367c43330e0065ec22538f545333b",
            "value": 0,
            "gas": "0x5d6a",
            "gasPrice": "0x3b9aca00",
            "data": "0xdb7eff7c00000000",
            "nonce": "0x2",
        }
        signature = wallet.sign_transaction(transaction_payload)
        expected_sig = {
            'rawTransaction': '0xf86b02843b9aca00825d6a94dea35e452b7367c43330e0065ec22538f545333b8088db7eff7c0000000026a0dc195956a449f5019aac98d79b50b742243224434d3c0a142c0177ffb30e3a95a00f62eaab7315a950af5735ad67be0eb7b95279514568eb8da91ca93b84c2dc7c',
            'hash': '0x616452f0874117edf0bf0c2f39f13d16a83748814f681efdc573431fc5088fb6',
            'r': 99553614456219982787208038055545973077114573530231040312394260751689716742805,
            's': 6959463372013131084391662123144090401008917770820119608199796736569070771324,
            'v': 38
        }
        self.assertEqual(signature, expected_sig)

    def test_wallet_sign_transaction_1559(self):
        wallet = Wallet()
        private_key = "1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67"
        wallet.generate_from_private_key(private_key)
        transaction_payload = {
            "chainId": "0x1",
            "to": "0xdea35e452b7367c43330e0065ec22538f545333b",
            "value": 0,
            "gas": "0x5d6a",
            "maxPriorityFeePerGas": "0x3b9aca00",
            "maxFeePerGas": "0x3b9aca00",
            "data": "0xdb7eff7c00000000",
            "nonce": "0x3",
        }
        signature = wallet.sign_transaction(transaction_payload)
        expected_sig = {
            'rawTransaction': '0x02f8720103843b9aca00843b9aca00825d6a94dea35e452b7367c43330e0065ec22538f545333b8088db7eff7c00000000c001a0a2bcfd31e17602c4e1a7ef22e2b4545f0819f9609e58d191b7e8c146b68b070fa053cae089a194142eff775deb9bdcdfc11db444ca2845d3536f25ee195d8a9c5a',
            'hash': '0xf3bfb32dbc6af1bb189fb264d40ff226af04ee6ff340585cbc38dc34222acc83',
            'r': 73608596205274428333047184892738464462600099222674297925900741474549985117967,
            's': 37900419241206913416517940217238883594964076317649986093305289145434189241434,
            'v': 1
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
