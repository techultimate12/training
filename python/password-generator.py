#Password Generator Project

import time
print("Welcome to Jack's Password Generator!")
time.sleep(2)
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
special = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']


password = ""
choice_l = int(input("How many letters do you want in your password?"))
for char in range(1, choice_l + 1):
   password += random.choice(letters)
choice_n = int(input("Now how many numbers do you want in your password?"))
for char in range(1, choice_n + 1):
   password += random.choice(numbers)
hoice_s = int(input("Special characters are important for password security, how many of those do you want?"))
for char in range(1, choice_n + 1):
   password += random.choice(special)

print("Generating password")
time.sleep(2)

print(password)