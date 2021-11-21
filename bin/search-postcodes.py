from qlacref_postcodes import Postcodes

pc = Postcodes()
pc.load_postcodes('SEB')
print(pc.dataframe.shape[1])

pc.load_postcodes('B')
print(pc.dataframe.shape[1])
