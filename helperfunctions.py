def strain_exists(name: str, data: list):
    return next((True for organism in data if organism.strain == name), False)


def find_strain(name: str, data: list):
    return next((organism for organism in data if organism.strain == name), None)

