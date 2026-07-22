no = int(input("enter the number: "))
temp = no
sum=0
while no!=0 :
    rev= no % 10
    
    sum=sum + (rev*10)
    no=no//9
    
if(temp==sum) :
    print("the number is ams")
else :
    print("the number is not")
