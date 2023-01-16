def strain_exists(name: str, data: list):
    return next((True for organism in data if organism.strain == name), False)


def find_strain(name: str, data: list):
    return next((organism for organism in data if organism.strain == name), None)

def get_complementary_string(sequence: str):
    complementary_string = ''
    for base in sequence[::-1]:
        match base:
            case 'A':
                complementary_string += 'T'
            case 'T':
                complementary_string += 'A'
            case 'C':
                complementary_string += 'G'
            case 'G':
                complementary_string += 'C'
            case 'N':
                complementary_string += 'N'

    return complementary_string