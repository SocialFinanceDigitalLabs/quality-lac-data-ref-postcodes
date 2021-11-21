import hashlib
from pathlib import Path

import rsa

import qlacref_postcodes
from qlacref_postcodes import Postcodes, alphabet

root_dir = Path(qlacref_postcodes.__file__).parent


def main(privkey):
    with open(root_dir / "hashes.txt", 'wt') as output:
        for letter in alphabet:
            filename = Path(root_dir / f"postcodes_{letter}.pickle.gz")
            if filename.is_file():
                with open(filename, 'rb') as file:
                    output.write(hashlib.sha512(file.read()).hexdigest())
                    output.write(' ')
                    output.write(filename.name)
                    output.write('\n')

    with open(root_dir / "hashes.txt", 'rb') as file:
        signature = rsa.sign(file, privkey, 'SHA-512')

    with open(root_dir / "hashes.sig", 'wt') as file:
        file.write(signature.hex())


if __name__ == "__main__":
    with open('id_rsa', 'rb') as key:
        privkey = rsa.PrivateKey.load_pkcs1(key.read())

    main(privkey)