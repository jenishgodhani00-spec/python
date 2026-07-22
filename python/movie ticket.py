age = int(input("enter the age of person: "))
print(age)

if age <= 5 :
    price = 'free'
elif age >= 5 and age <= 12 :
    price = 100
elif age >= 13 and age <= 59 :
    price = 200
else :
    price = 150

print("price of ticket is ",price)