'''
http://www.tumblr.com/login
under lib/site-packages rename crypto folder to Crypto
'''
from Crypto.PublicKey import RSA

new_key = RSA.generate(2048, e=65537)
public_key = new_key.publickey().exportKey("PEM")
private_key = new_key.exportKey("PEM")

print public_key
print private_key

f = open('publickeyfile.pem', 'wb')
f.write(public_key)
f.close()

f = open('privatekeyfile.pem', 'wb')
f.write(private_key)
f.close()