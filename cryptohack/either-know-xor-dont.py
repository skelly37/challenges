from pwn import xor

FLAG = bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")

#lmao
print(xor(KEY, "crypto{"))
print(xor(KEY, "myXORkey"))
