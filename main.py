import argparse as arg
import classes.gffClasses as Gffclasses
import time


parser = arg.ArgumentParser()
parser.add_argument('file', type=str, help='filepath needed')

args = parser.parse_args()


def strain_exists(name: str, data: list):
    return next((True for organism in data if organism.strain == name), False)


def find_strain(name: str, data: list):
    return next((organism for organism in data if organism.strain == name), None)


def add_sequence(data: list, dna_seq: str, fasta_counter: int):

    if dna_seq != '':
        tmp_organism: Gffclasses.Organism = find_strain(name=data[fasta_counter].strain,
                                                        data=data)
        tmp_organism.fasta += dna_seq
        dna_seq = ''
    return dna_seq


def build_gff_class():
    organism_list = []
    dna_seq = ''

    with open(args.file) as gff3:
        fasta_extract = False
        fasta_counter = -2

        for line in gff3.readlines():
            if line.startswith("##sequence-region"):
                strain = line.split(" ")
                tmp_organism = Gffclasses.Organism()
                tmp_organism.strain = strain[1]
                organism_list.append(tmp_organism)

            elif strain_exists(line.split("\t")[0], organism_list):
                gffrow = line.split("\t")
                tmp_organism: Gffclasses.Organism = find_strain(name=gffrow[0], data=organism_list)
                tmp_organism.gff_data.append(Gffclasses.GffData(gffrow=gffrow))

            elif line.startswith('##FASTA'):
                fasta_extract = True

            elif line.startswith('>'):
                fasta_counter += 1
                dna_seq = add_sequence(data=organism_list, dna_seq=dna_seq, fasta_counter=fasta_counter)

            elif fasta_extract and not line.startswith('>'):
                dna_seq += line.strip('\n')

    add_sequence(data=organism_list, dna_seq=dna_seq, fasta_counter=fasta_counter + 1)

    for element in organism_list:
        element.set_annotated_dna_seq()

    return organism_list


if __name__ == "__main__":

    start_time = time.time()
    organism_list = build_gff_class()

    print("--- %s seconds ---" % (time.time() - start_time))
