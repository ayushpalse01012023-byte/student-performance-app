import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df= pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
print(df)
print(df.head())

df["Age"].fillna(df["Age"].mean(), inplace = True )
df.drop("Cabin", axis = 1, inplace = True )
df["Embarked"].fillna(df["Embarked"].mode()[0])

print(df.head())