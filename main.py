import argparse as arg
import classes.gffClasses as Gffclasses
import time
from helperfunctions import find_strain, strain_exists, print_multiple_fasta


parser = arg.ArgumentParser()
parser.add_argument('file', type=str, help='filepath needed')
parser.add_argument('-f', '--fasta', action='store_true', help='Set Flag for a Fasta extraction')


args = parser.parse_args()


def add_sequence(data: list, dna_seq: str, fasta_counter: int, printable_seq: str):

    if dna_seq != '':
        tmp_organism: Gffclasses.Organism = find_strain(name=data[fasta_counter].strain,
                                                        data=data)
        tmp_organism.fasta += dna_seq
        tmp_organism.printable_fasta += printable_seq
        dna_seq = ''
    return dna_seq


def build_gff3_class():

    organism_class_objects = []
    dna_seq = ''
    printable_seq = ''

    with open(args.file) as gff3:
        fasta_extract = False
        fasta_counter = -2

        for line in gff3.readlines():
            if line.startswith("##sequence-region"):
                strain = line.split(" ")
                tmp_organism = Gffclasses.Organism()
                tmp_organism.strain = strain[1]
                organism_class_objects.append(tmp_organism)

            elif strain_exists(line.split("\t")[0], organism_class_objects):
                gffrow = line.split("\t")
                tmp_organism: Gffclasses.Organism = find_strain(name=gffrow[0], data=organism_class_objects)
                tmp_organism.gff_data.append(Gffclasses.GffData(gffrow=gffrow))

            elif line.startswith('##FASTA'):
                fasta_extract = True

            elif line.startswith('>'):
                fasta_counter += 1
                dna_seq = add_sequence(data=organism_class_objects, dna_seq=dna_seq, fasta_counter=fasta_counter,
                                       printable_seq=printable_seq)

            elif fasta_extract and not line.startswith('>'):
                dna_seq += line.strip('\n')
                if args.fasta:
                    printable_seq += line

    add_sequence(data=organism_class_objects, dna_seq=dna_seq, fasta_counter=fasta_counter + 1,
                 printable_seq=printable_seq)

    for element in organism_class_objects:

        element.set_annotated_dna_seq(fasta_extract=args.fasta, filename=args.file.split('/')[-1])

    return organism_class_objects

def build_sc_class():

    object_handler = []

    with open(args.file) as gtf_file:

        for line in gtf_file:
            gtf_row = line.split('\t')
            object_handler.append(Gffclasses.GffData(gffrow=gtf_row))
    for row in object_handler:
        if row.feature_type == 'promotors':
            print(row.feature_type)


if __name__ == "__main__":

    start_time = time.time()

    build_sc_class()

    #organism_list = build_gff3_class()
    #print_multiple_fasta(data_list=organism_list, filename=args.file.split('/')[-1])

    print("--- %s seconds ---" % (time.time() - start_time))
