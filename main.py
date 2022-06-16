import argparse as arg

parser = arg.ArgumentParser()
parser.add_argument('file', type = str, help = 'Dateipfad zur Datei')

args = parser.parse_args()


## TO-DO:
##
##
##



class Gff_data:
    def __init__(self, seq_id, source, feature_type, feature_start, feature_end, score, strand, phase, atributes):
        self.seq_id = seq_id
        self.source = source
        self.feature_type = feature_type
        self.feature_start = feature_start
        self.feature_end = feature_end
        self.score = score
        self.strand = strand
        self.phase = phase
        self.atributes = atributes
        #self.row_entrys = row_entrys

def read():

    class_per_region = []

    with open(args.file) as gff3:
        for line in gff3.readlines():
            if line.startswith('##sequence-region'):
                seq_region = Gff_data(line.split()[1])
                class_per_region.append(seq_region)

                print(seq_region.seq_id)

    print(class_per_region)




if __name__ == "__main__":
    read()