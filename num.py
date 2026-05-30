import numpy as np 

marks = [10 , 55, 77, 88, 99, 34 ]

arr = np.array(marks)

mean = np.mean(marks)
print(mean)
n = np.median(marks)
print(n)

vars = np.var(marks)
print(vars)

you = np.std(marks)
print(you)