import argparse as arg
import classes.gffClasses as bact

parser = arg.ArgumentParser()
parser.add_argument('file', type=str, help='Dateipfad zur Datei')

args = parser.parse_args()


## TO-DO:
##
##
##


def bacteria_exists(name: str, bacteria_list: list):
    return next((True for bacteria in bacteria_list if bacteria.region == name), False)


def find_bacteria(name: str, bacteria_list: list):
    return next((bacteria for bacteria in bacteria_list if bacteria.region == name), None)


def read():
    dataset_counter = 0
    fasta_counter = 1
    bacteria_list = []
    dna_seq = ''
    with open(args.file) as gff3:
        fasta_extract = False

        for index, line in enumerate(gff3.readlines()):
            if line.startswith("##sequence-region"):
                lineSplit = line.split(" ")
                tmp_bacteria = bact.Bacteria()
                tmp_bacteria.region = lineSplit[1]
                bacteria_list.append(tmp_bacteria)
            elif bacteria_exists(line.split("\t")[0], bacteria_list):
                seq_id = line.split("\t")
                tmp_bacteria: bact.Bacteria = find_bacteria(name=seq_id[0], bacteria_list=bacteria_list)
                tmp_bacteria.gff_data.append(bact.GffData(seq_id=seq_id))
            elif line.startswith('##FASTA'):
                fasta_extract = True
            elif line.startswith('>'):
                dataset_counter += 1
                if dna_seq:
                    dna_seq = ''
            elif fasta_extract and not line.startswith('>'):
                dna_seq += line.strip('\n')

    for bacteria in bacteria_list:
        gff_data:bact.GffData = bacteria.gff_data[0]
        gff_data: list[bact.GffData] = bacteria.gff_data
        for gff in gff_data:
            print(gff.attributes)
        # print(gff_data.attributes)


if __name__ == "__main__":
    read()
