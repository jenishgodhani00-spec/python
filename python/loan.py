income = int(input("enter the income of the person: "))
print(income)

if income >= 100000 :
    loan = 'premium loan'
elif income >= 50000 :
    loan = 'standerend loan'
elif income >= 25000 :
    loan = 'basic loan'
else :
    loan = 'not eligible'

print("the loan you get is : ",loan)