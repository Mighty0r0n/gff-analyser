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


def print_multiple_fasta(data_list: list, filename: str):
    with open(filename.replace('.gff3', '.mpfa'), 'w') as file:
        for element in data_list:

            file.write("##sequence-region   {}\n".format(element.strain))

            for entry in element.gff_data[1:]:
                file.write(">{}\n{}\n".format(entry.attributes[0].split('=')[-1], entry.dnaseq))
