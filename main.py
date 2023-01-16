import argparse as arg
import gc
import os
from classes import gffClasses as gffClasses
import time
from helperfunctions import find_strain, strain_exists


parser = arg.ArgumentParser()
parser.add_argument('file', type=str, help='filepath needed')
parser.add_argument('-f', '--fasta', action='store_true', help='Set Flag for a Fasta extraction')


args = parser.parse_args()

file = args.file
fasta = args.fasta

def add_sequence(data: list, dna_seq: str, fasta_counter: int, printable_seq: str):

    if dna_seq != '':
        tmp_organism: gffClasses.Organism = find_strain(name=data[fasta_counter].strain,
                                                        data=data)
        tmp_organism.fasta += dna_seq
        tmp_organism.printable_fasta += printable_seq
        dna_seq = ''
    return dna_seq

def header_check():

    with open(args.file, 'r') as file:
        return (True if not file.readline().startswith('#') else False)

        # if not file.readline().startswith('#'):
        #     return False
        # return True
def build_gff3_class(file):

    organism_class_objects = []
    dna_seq = ''
    printable_seq = ''

    gff3_gen = (row for row in open(file).readlines())

    headerless_file = header_check()

   # with open(file) as gff3_gen:
    fasta_extract = False
    fasta_counter = -2



    #change

    # Check if the input is a headerless file
    if headerless_file:

        tmp_organism = gffClasses.Organism()
        tmp_organism.strain = file.split('\\')[-1]

        organism_class_objects.append(tmp_organism)

    for line in gff3_gen:


        if line.startswith("##sequence-region"):
            strain = line.split(" ")
            tmp_organism = gffClasses.Organism()
            tmp_organism.strain = strain[1]
            organism_class_objects.append(tmp_organism)

        # Possible Bug, if headerless file contains a sequence
        elif strain_exists(line.split("\t")[0], organism_class_objects) or headerless_file:
            gffrow = line.split("\t")
            if not headerless_file:
                tmp_organism = find_strain(name=gffrow[0], data=organism_class_objects)

            tmp_organism.gff_data.append(gffClasses.GffData(gffrow=gffrow))



        elif line.startswith('##FASTA') and not headerless_file:
            fasta_extract = True

        elif line.startswith('>') and not headerless_file:
            fasta_counter += 1
            dna_seq = add_sequence(data=organism_class_objects, dna_seq=dna_seq, fasta_counter=fasta_counter,
                                   printable_seq=printable_seq)

        elif fasta_extract and not line.startswith('>'):
            dna_seq += line.strip('\n')
            if fasta:
                printable_seq += line

    add_sequence(data=organism_class_objects, dna_seq=dna_seq, fasta_counter=fasta_counter + 1,
                 printable_seq=printable_seq)


    for element in organism_class_objects:

        element.set_annotated_dna_seq(fasta_extract=fasta, filename=file.split('/')[-1])
    gc.collect()
    return organism_class_objects

# not needed right now, delete after gene bug
def build_sc_class(features: list):

    object_handler = []

    header_check = False

    test = 'gff-files\\homo_sapiens.104.promoters2000.gtf'

    with open(test) as gtf_file:



        for line in gtf_file:
            gtf_row = line.split('\t')
            object_handler.append(gffClasses.GffData(gffrow=gtf_row))

    for feature in features:

        line_count = 0
        gene_count = 0
        for row in object_handler:
            line_count += 1

            # ONLY the gene's are counted +1 more than they are... Why?!?!
            if row.feature_type == feature:
                gene_count += 1

        if feature == 'gene':
            print(line_count, '  Lines')
        print(gene_count, ' ', feature)

def test():
    return print('Error')

def get_out_file_names():
    test = os.listdir('out')

    feature_list = []

    for line in test:
        foo = line.strip('.gtf')
        bar = foo.split('.')
        print(bar[-1])
        feature_list.append(bar[-1])

    return feature_list

if __name__ == "__main__":

    start_time = time.time()

    #header_check()

    #get_out_file_names()
    #
    #
    organism_list = build_gff3_class(file=args.file)
    #
    #
    #
    #
    # #
    # #
    # #
    for element in organism_list:
        features = element.count_features()
        #element.generate_feature_gtf(gffdata_list=organism_list, feature_keys=features)
        element.generate_promotor_gtf(gffdata_list=organism_list)
        element.generate_tss_gtf(gffdata_list=organism_list)

    #print_multiple_fasta(data_list=organism_list, filename=args.file.split('/')[-1])

    print("--- %s seconds ---" % (time.time() - start_time))
