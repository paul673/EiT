import json
 

def get_periodic_table(): 
    # Opening JSON file
    f = open('data/pt.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Closing file
    f.close()
    pt = {}
    for i in data:
        pt[i['symbol']] = i
    return pt


# Molar mass
molar_mass = {
    'Ca': 40.078,
    'O': 15.999,
    'C': 12.011,
}
