#!/usr/bin/env python3
import ecdsa


class Wallet:

    def __init__(self):
        self.signing_key = None
        self.verifying_key = None
    
    # Generate Private and Public keys using ECDSA
    def generate_keys(self):
        self.signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.verifying_key = self.signing_key.get_verifying_key()
    
    # Given a message string, returns signature
    def sign_message(self, message):
        signed_message = self.signing_key.sign(bytes(message, 'utf-8'))
        return signed_message

    # Given a signature, sender public key, and message returns if signature is valid
    def verify_message(self, signature, sender_verifying_key, message):
        try:
            sender_verifying_key.verify(signature, bytes(message, 'utf-8'))
        except:
            return False
        return True
