import argparse as arg
import classes.gffClasses as bact
import time


parser = arg.ArgumentParser()
parser.add_argument('file', type=str, help='Dateipfad zur Datei')

args = parser.parse_args()


## TO-DO:
##
##  \n rausnehmen
##


def bacteria_exists(name: str, bacteria_list: list):
    return next((True for bacteria in bacteria_list if bacteria.region == name), False)


def find_bacteria(name: str, bacteria_list: list):
    return next((bacteria for bacteria in bacteria_list if bacteria.region == name), None)


def read():

    bacteria_list = []


    with open(args.file) as gff3:
        fasta_extract = False
        dna_seq = ''
        fasta_counter = -1
        for line in gff3.readlines():
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
                fasta_counter += 1
                if dna_seq != '':
                    tmp_bacteria: bact.Bacteria = find_bacteria(name=bacteria_list[fasta_counter].region, bacteria_list=bacteria_list)
                    tmp_bacteria.fasta += dna_seq
                    dna_seq = ''

            elif fasta_extract and not line.startswith('>'):
                dna_seq += line.strip('\n')




if __name__ == "__main__":
    start_time = time.time()

    read()
    print("--- %s seconds ---" % (time.time() - start_time))

