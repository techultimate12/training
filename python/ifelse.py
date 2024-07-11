age = int(input("Enter your age:"))
if age == 1:
  print("you really young")
elif age > 1 and age < 18:
  print("you young")
elif age >= 18 and age < 50:
  print("you an adult")
else:
  print("you an old man")
