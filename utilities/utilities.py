import string
from data.data import get_periodic_table

def add_to_dict(d, key, value):
    if key in d.keys():
        d[key] += value
    else:
        d[key] = value
    return d

def get_molecule_dict(molecule):
    """
    Creates a dictionary containing the amount of specific atoms in a molecule.
    C6H10O5 would return {'C': 6, 'H': 10, 'O': 5}
    """

    # Dictionary to contain everything
    elemtsd = {}

    # String to store the current letter necessary to keep track of elements containing more than one letter (Ca)
    current_element= ''

    # Iterate though all characters in the molecules formula 
    for index, caracter in enumerate(molecule):
        # Check if the character is uppercase. This would indicate that a new element starts
        if caracter in string.ascii_uppercase:
            # Reset the current element variable and populate it with the current character
            current_element = caracter
            # Check if we reached the end of the formula. The current caracter cannot have any follwing letters or numbers and can be added to the dictonary.
            if index == len(molecule)-1:
                elemtsd = add_to_dict(elemtsd, current_element, 1)
            else:
                # Check if this is the last letter of the current atom.
                if molecule[index+1] in string.ascii_uppercase or  molecule[index+1].isnumeric():
                    # Check if there is a number behind the current atom and find the number
                    condition = molecule[index+1]
                    number = ''
                    iteration_index = 1
                    if molecule[index+1].isnumeric():
                        while condition.isnumeric():
                            
                            number = number + molecule[index+iteration_index]
                            iteration_index += 1
                            if index + iteration_index  < len(molecule):
                                condition = molecule[index+iteration_index]
                            else:
                                condition="a"

                        elemtsd = add_to_dict(elemtsd, current_element, int(number))
                    else:
                        #add element to dictionary
                        elemtsd = add_to_dict(elemtsd, current_element, 1)
        elif not caracter.isnumeric():
            current_element = current_element + caracter
            if index == len(molecule)-1:
                #elements.append(current_element)
                elemtsd = add_to_dict(elemtsd, current_element, 1)
            else:
                if molecule[index+1] in string.ascii_uppercase  or  molecule[index+1].isnumeric(): 
                    #elements.append(current_element)
                    if molecule[index+1].isnumeric():
                        condition = molecule[index+1]
                    number = ''
                    iteration_index = 1
                    if molecule[index+1].isnumeric():
                        while condition.isnumeric():
                            
                            number = number + molecule[index+iteration_index]
                            iteration_index += 1
                            if index + iteration_index  < len(molecule):
                                condition = molecule[index+iteration_index]
                            else:
                                condition="a"

                        elemtsd = add_to_dict(elemtsd, current_element, int(number))
                    else:
                        elemtsd = add_to_dict(elemtsd, current_element, 1)

    return elemtsd

def get_mmass(molecule):

    elements = get_molecule_dict(molecule)
    #print(elements)
    
    molar_mass = 0
    for element, amount in elements.items():
        element_molar_mass = float(get_periodic_table()[element]['atomicMass'].split("(")[0])
        molar_mass = molar_mass + element_molar_mass*amount
    return molar_mass

def get_co2_content(molecule):
    elements = get_molecule_dict(molecule)
    if ("C" in elements.keys()) and ("O" in elements.keys()):
        return int(min(elements["C"], elements["O"]/2))
    else:
        return 0
    

def co2_per_mass(mass, molecule): #mass in g
    co2_content = get_co2_content(molecule)
    moles = mass/get_mmass(molecule)
    return moles*get_mmass('CO2')*co2_content
        


if __name__ == "__main__":
    print(get_mmass('CaO2'))
    print(get_periodic_table())