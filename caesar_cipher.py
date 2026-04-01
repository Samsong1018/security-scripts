#!/usr/bin/env python3


def caesar(text: str, shift: int, decrypt: bool = False) -> str:
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


def rot13(text: str) -> str:
    return caesar(text, 13)


def brute_force(text: str) -> list[tuple[int, str]]:
    return [(shift, caesar(text, shift, decrypt=True)) for shift in range(1, 26)]


if __name__ == '__main__':
    print("Caesar Cipher")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. ROT13")
    print("4. Brute-force decode")
    choice = input("Choose (1/2/3/4): ").strip()

    text = input("Enter text: ")

    if choice == '1':
        shift = int(input("Enter shift (1-25): "))
        print("Result:", caesar(text, shift))
    elif choice == '2':
        shift = int(input("Enter shift (1-25): "))
        print("Result:", caesar(text, shift, decrypt=True))
    elif choice == '3':
        print("Result:", rot13(text))
    elif choice == '4':
        print("All possible decodes:")
        for shift, decoded in brute_force(text):
            print(f"  Shift {shift:2d}: {decoded}")
