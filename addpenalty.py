import pandas as pd
import tasks as tsk


def set_penalty(row, lows, highs):
    if row.place == "cruise ship":
        return tsk.cruise_utility
    elif row.place in lows:
        return tsk.low_penalty
    elif row.place in highs:
        return tsk.high_penalty
    else:
        return row.update_utility


low = [
         "Plaça de Cort",
         "Plaça de toros de Palma",
         "Plaza Del Mercat",
         "Plaça del Rei Joan Carles I"
        ]
high = [
         "Catedral-Basílica de Santa María de Mallorca",
         "Castell de Bellver",
         "Royal Palace of La Almudaina",
         "Museu Fundación Juan March, Palma",
         "Museo de Mallorca",
         "Museu Diocesà de Mallorca"
        ]


if __name__ == "__main__":
    topsights = pd.read_csv(
                "palmadata/palmapointsofinterest_cleaned.csv",
                header=0,
                dtype={
                    "place": 'str',
                    "description": 'str',
                    "latitude": 'float',
                    "longitude": 'float',
                    "stars": 'float',
                    "reviews": 'float'
                }
            )

    topsights["update_utility"] = tsk.standard_penalty
    topsights["update_utility"] = topsights.apply(lambda row: set_penalty(row, low, high), axis=1)
    topsights.to_csv('palmadata/palmapointsofinterest_cln_pnl.csv', index=False)
