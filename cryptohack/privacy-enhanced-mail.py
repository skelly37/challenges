from Crypto.PublicKey.RSA import importKey

file_contents = open("privacy_enhanced_mail.pem").read()
print(importKey(file_contents).d)
