unit =int(input("enter total number of unit:"))
print(unit)

if unit <=100 :
    total_amount=(unit*2)
elif unit <= 200 :
    total_amount= (100*2) + (unit-100)*3
elif unit <= 300 :
    total_amount= (100*2) + (100*3) + (unit-200)*4
else :
    total_amount= (100*2) + (100*3) + (100*4) + (unit-300)*7

print("total electricity amout is ", total_amount)
