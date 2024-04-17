import os
import sys

from cryptography.hazmat.primitives import serialization
from django.core.management import BaseCommand
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

from auth.settings import RSA_KEY_DIR, RSA_PRIVATE_KEY_FILE, RSA_PUBLIC_KEY_FILE


class Command(BaseCommand):
    help = 'Generate a new RSA key pair'

    def handle(self, *args, **options):

        if os.path.exists(RSA_KEY_DIR):
            self.stdout.write('RSA key directory already exists', style_func=self.style.WARNING)
            if os.path.exists(RSA_PRIVATE_KEY_FILE) and os.path.exists(RSA_PUBLIC_KEY_FILE):
                self.stdout.write('RSA Key pair already exists', style_func=self.style.ERROR)
                sys.exit(1)
        else:
            os.makedirs(RSA_KEY_DIR)
            # generate private key
            private_key= rsa.generate_private_key(public_exponent=65537, key_size=4096,
                                                  backend=default_backend())
            # serialize private key
            private_key_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                        encryption_algorithm=serialization.NoEncryption())
            # get public key for private key
            public_key = private_key.public_key()

            # serializer public key
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # write private key to file
            with open(RSA_PRIVATE_KEY_FILE, 'w') as f:
                f.write(private_key_pem.decode())

            # write public key to file
            with open(RSA_PUBLIC_KEY_FILE, 'w') as f:
                f.write(public_key_pem.decode())

            self.stdout.write('RSA Key pair generated', style_func=self.style.SUCCESS)
            sys.exit(0)