"""Wallet Handler"""
import ecdsa

class Wallet(object):
    """Handles all Authentication Stuff"""

    def __init__(self):
        self.signing_key = None
        self.verifying_key = None

    def generate_keys(self):
        """Generate Private and Public keys using ECDSA"""
        self.signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.verifying_key = self.signing_key.get_verifying_key()

    def sign_message(self, message):
        """Given a message string, returns signature"""
        if self.signing_key != None:
            signed_message = self.signing_key.sign(bytes(message, 'utf-8'))
            return (True, signed_message)
        else:
            return (False, "Keys not generated")

    @staticmethod
    def verify_message(signature, sender_verifying_key, message):
        """Given a signature, sender public key, and message returns if signature is valid"""
        try:
            sender_verifying_key.verify(signature, bytes(message, 'utf-8'))
        except GeneratorExit:
            return False
        return True
