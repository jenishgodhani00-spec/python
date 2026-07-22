speed = int(input("enter the speed of vehicle: "))
print(speed)

if speed<=60 :
    fine=0
elif speed>=61 and speed<=80 :
    fine =500
elif speed>=81 and speed<=100 :
    fine=1000
else :
    fine=2000

print("the fine is ", fine)
