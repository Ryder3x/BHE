# -*- coding: utf-8 -*-
import lzma
import base64 as b64
import random as rd
import argparse
"""
Copyright owned by Ryder3x

----------------------------------------------------------------------------
File: BHE.py
Author: Ryder3x
Created: 13th June 2023
Copyright owned by Ryder3x

Description: This is the source code of the BHE tool. All intellectual
             property rights are owned by the author. Any unauthorized copying,
             modification, or distribution without prior written permission from
             the author is strictly prohibited.
----------------------------------------------------------------------------
"""

orig_map={"A":"\u034F","B":"\u200C","C":"\u200E","D":"\u200D","E":"\u202A","F":"\u202B","G":"\u202C","H":"\u202D","I":"\u202E","J":"\u2060","K":"\u2061","L":"\u2062","M":"\u2063","N":"\u2064","O":"\u2065","P":"\u2066","Q":"\u2067","R":"\u2068","S":"\u2069","T":"\u180E","U":"\u200B","V":"\u206A","W":"\u206B","X":"\u206C","Y":"\u206D","Z":"\u206E","0":"\u034F\u206F","1":"\u200C\u206F","2":"\u200E\u206F","3":"\u200D\u206F","4":"\u202A\u206F","5":"\u202B\u206F","6":"\u202C\u206F","7":"\u202D\u206F","8":"\u202E\u206F","9":"\u2060\u206F","=":"\u180B"}

IPR = "\n\n\n# MÃ HÓA HỐ ĐEN (BHE) TẠO BỞI @Ryder3x (https://github.com/)"


def new_map(m, pwd):
    rd.seed(pwd)
    ks = list(m.keys())
    rd.shuffle(ks)
    m = {k: m[ks[i]] for i, k in enumerate(m)}
    return m

def enc(t):
    t = lzma.compress(t.encode("utf-8"), preset=9)
    b32 = b64.b32encode(t).decode("utf-8")
    return b32

def dec(t):
    t = b64.b32decode(t.encode("utf-8"))
    de = lzma.decompress(t).decode("utf-8")
    return de

def encode(t, m):
    e = ""
    for _ in enc(t):
        if _ in m:
            e += m[_]
        else:
            e += _
    return f"${e}"

def decode(t, m):
    e, i, t = "", 0, t[1:]
    while i < len(t):
        _ = t[i:i+2] if t[i:i+2] in m.values() else t[i]
        e += list(m.keys())[list(m.values()).index(_)]
        i += 2 if _ == t[i:i+2] else 1
    return dec(e)

def Encode(key, text):
	map = new_map(orig_map, key)
	enc = encode(f"{text}{IPR}", map)
	return enc

def Decode(key, text):
	map = new_map(orig_map, key) 
	dec = decode(text, map)
	return dec

def fileEncode(key, file):
	map = new_map(orig_map, key)
	data = open(f"{file}","r").read()
	open(f"BHE_ENC_{file}.txt","w").write(encode(f"{data}{IPR}", map))
	print(f"save encode file at BHE_ENC_{file}.txt")

def fileDecode(key, file):
	map = new_map(orig_map, key)
	data = open(f"{file}","r").read()
	open(f"BHE_DEC_{file}.txt","w").write(decode(data, map))
	print(f"save decode file at BHE_DEC_{file}.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BHE Tool")
    parser.add_argument("--encode", action="store_true", help="Encode file mode")
    parser.add_argument("--decode", action="store_true", help="Decode file mode")
    parser.add_argument("-f", "--file", type=str, help="Input file")
    parser.add_argument("-k", "--key", type=str, help="Encryption/Decryption key")

    args = parser.parse_args()

    if args.encode:
        if args.file and args.key:
            fileEncode(args.key, args.file)
        else:
            print("Please provide both file (-f/--file) and key (-k/--key) arguments for encoding.")
    elif args.decode:
        if args.file and args.key:
            fileDecode(args.key, args.file)
        else:
            print("Please provide both file (-f/--file) and key (-k/--key) arguments for decoding.")
    else:
        print("Please specify either --encode or --decode.")

