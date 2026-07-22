marks = int(input("enter the marks of student"))
print(marks)
if marks >= 90 :
    grade = 'A' 
elif marks>= 80 :
    grade = 'B'
elif marks >= 70 :
    grade = 'C'
elif marks >= 60 :
    grade = 'D'
else :
    grade = 'F'

print("student gread is ", grade)