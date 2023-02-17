import pandas as pd

configurations = pd.read_json('config.json', dtype={
    'tipo': str,
})


def find_register(data):
    id_register = data[:2]
    element = configurations.loc[configurations['tipo'] == id_register]
    return element.to_dict('records')[0]
