from sklearn.linear_model import LinearRegression

X = [[1] ,[2], [3], [4] ,[5] ,[6]]
y=[10, 15, 16, 20, 30, 35]

mdl = LinearRegression()
mdl.fit(X,y)

hours = input("Enter the hours your studied : ")

marks = mdl.predict([[hours]])
print(f"when you studied for {hours} hours then you will get {marks} marks ")
