n =int(input("enter the number: "))
a=1
b=2
c = None
print(a, end=" ")
print(b, end=" ")
while 1:
    c=a+b
    a=b
    b=c
    if(c>n) :
        break
    else :
        print(c, end="  ")
        