import random
from .Modules import pandas as pd

Data = pd.read_excel('Dummy Coordinates.xlsx')
X = Data['X'].tolist()
Y = Data['Y'].tolist()
Z = Data['Z'].tolist()
print( X, Y, Z)