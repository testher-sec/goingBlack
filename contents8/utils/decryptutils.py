'''
http://www.tumblr.com/login
under lib/site-packages rename crypto folder to Crypto
'''
import sys
import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def decrypt(encrypted):
    private_key = "PASTEPRIVATEKEYHERE"

    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    chunk_size = 256
    offset = 0
    decrypted = ""
    encrypted = base64.b64decode(encrypted)

    while offset<len(encrypted):
        decrypted += rsakey.decrypt(encrypted[offset:offset+chunk_size])
        offset += chunk_size

    # now we decompress the original
    plaintext = zlib.decompress(decrypted)

    print plaintext


if __name__ == "__main__":
    try:
        encrypted = sys.argv[1]
    except IndexError:
        print "USE: " + sys.argv[0] + " <encrypted-text>"
        sys.exit(0)
    decrypt(encrypted)
    sys.exit(0)