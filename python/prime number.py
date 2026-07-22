n=int(input("enter the number: "))
cnt=0
for i in range(1,n+1) :
    if(n%i==0) :
        cnt+=1
    if(cnt>2):
        break;
print(cnt)
if(cnt==2):
    print(n,"prime number")
else :
    print(n,"not a prime number")

