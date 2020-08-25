import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

palmasights_google = "https://www.google.com/travel/things-to-do/see-all?g2lb=2502548%2C4258168%2C4260007%2C4270442%2C4274032%2C4305595%2C4306835%2C4317915%2C4319921%2C4328159%2C4364504%2C4366684%2C4367954%2C4371335%2C4381263%2C4386665%2C4395590%2C4398672%2C4401769%2C4403882%2C4270859%2C4284970%2C4291517%2C4307997&hl=en&gl=es&un=1&otf=1&dest_mid=%2Fm%2F0jwz5&dest_state_type=sattd&sa=X&ved=0ahUKEwijqJaO1crqAhWMkxQKHRhlDnYQx2gIFg#ttdm=39.568471_2.647707_15&ttdmf=%252Fm%252F0lkjv"
palmatopsights = requests.get(palmasights_google)
soup_palma = BeautifulSoup(palmatopsights.content, 'html.parser')

data = soup_palma.find_all("script")[-3]
data_string = data.get_text()
data_list = eval(data_string[data_string.find("data:")+5:data_string.rfind("]")+1]
                 .replace("null", "'null'")
                 .replace("false", "'false'")
                 .replace("true", "'true'")
                 )


def valueifnull(value, idx=0):
    if value == "null":
        return np.nan
    elif type(value) == list:
        return value[idx]
    else:
        return value


dataframe = pd.DataFrame({
    "place": pd.Series([], dtype='str'),
    "description": pd.Series([], dtype='str'),
    "latitude": pd.Series([], dtype='float'),
    "longitude": pd.Series([], dtype='float'),
    "stars": pd.Series([], dtype='float'),
    "reviews": pd.Series([], dtype='float')
})

pointsofinterest = data_list[0][0][0][9][0]
for pointinfo in pointsofinterest:
    point = {
        "place":  valueifnull(pointinfo[0][1]),
        "description":  valueifnull(pointinfo[0][2]),
        "latitude": valueifnull(pointinfo[0][15], 0),
        "longitude": valueifnull(pointinfo[0][15], 1),
        "stars": valueifnull(pointinfo[0][25], 0),
        "reviews": valueifnull(pointinfo[0][25], 1)
    }
    dataframe = dataframe.append(point, ignore_index=True)

dataframe.to_csv('palmadata/palmapointsofinterest.csv', index=False)
