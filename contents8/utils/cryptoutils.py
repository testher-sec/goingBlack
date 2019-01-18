'''
http://www.tumblr.com/login
under lib/site-packages rename crypto folder to Crypto
'''
import zlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzxomotzRtkfd9Ut6FjZa" \
             "03L/NQaPJ4P69Gxy2zVi8IEw94sBXJpxBXNBebm1TqhZsNQdTsbM8b8kg4kA+Kum" \
             "sgsdRB3cNJhd1nV47CP+1SJsnn1UTWceq7/LiWHQH68+bPVkLg4HVhKDnKHX1ODP" \
             "2fJ8vbaiba+gAvQZBDRgvcfeT972O8iMV7Yvl+InNI6hX/IwWbI2vPAMT/vcyi2z" \
             "jygi9VUIc1Ri/XUk3mWVav27fX7cdcUIbFlotn5PGRecf3VV9MG+kAtOgRXSh0qC" \
             "HENqV0ZLeuvWczvI1jE98vj0pawJ87n9eqwhqQUAjgS82vU97AIEWrITsEwR8ayT" \
             "BQIDAQAB"

# needs https://www.microsoft.com/en-us/download/details.aspx?id=44266
# chunk_size = 256 is the maximum size for RSA encryption using pycrypto

def encrypt_string(plaintext):
    chunk_size = 256
    print "Compressing: %d bytes" % len(plaintext)
    plaintext = zlib.compress(plaintext)

    print "Encrypting %d bytes" % len(plaintext)

    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    encrypted = ""
    offset = 0

    # we encrypt in chunks of chunk_size (256)
    while offset < len(plaintext):
        chunk = plaintext[offset:offset+chunk_size]

        # fill it up with spaces until the size is 'chunk-size 256'
        if len(chunk) % chunk_size != 0:
            chunk += " " * (chunk_size - len(chunk))

        encrypted += rsakey.encrypt(chunk)
        offset += chunk_size

    encrypted = encrypted.encode("base64")

    print "Base64 encoded crypto: %d" % len(encrypted)
    return encrypted


def encrypt_post(filename):
    # open and read the file
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()

    encrypted_title = encrypt_string(filename)
    encrypted_body = encrypt_string(contents)

    return encrypted_title, encrypted_body

