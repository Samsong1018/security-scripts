#!/usr/bin/env python3

def caesar(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


if __name__ == '__main__':
    print("Caesar Cipher")
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose (1/2): ").strip()

    text = input("Enter text: ")
    shift = int(input("Enter shift (1-25): "))

    if choice == '2':
        print("Result:", caesar(text, shift, decrypt=True))
    else:
        print("Result:", caesar(text, shift))
