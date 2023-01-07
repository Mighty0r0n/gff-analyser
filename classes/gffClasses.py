#from helperfunctions import get_complementary_string


# to-do set dna seq in GffData umlagern // May set only a warning if no fasta is provided

class GffData:
    def __init__(self, gffrow):
        self._seq_id = gffrow[0]
        self._source = gffrow[1]
        self._feature_type = gffrow[2]
        self._feature_start = gffrow[3]
        self._feature_end = gffrow[4]
        self._score = gffrow[5]
        self._strand = gffrow[6]
        self._phase = gffrow[7]
        self._attributes = gffrow[8].split(";")
        self._dnaseq = ''

    def get_complementary_string(self, sequence: str):
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

    def get_whole_line(self):

        tmp_attribute = ''


        # Warum sind in den gff3 files die Attribute ohne ; am Ende aber in den gtf's mit??
        # Bug hier noch in der Darstellung für gff3 files

        # Adding list object to tmp_string to get a printable attribute line
        for entry in self.attributes:
            tmp_attribute += entry

            # Adding at last entry ; for formating purposes
            if entry != entry[-1]:
                tmp_attribute += ';'


        whole_line = (self.seq_id + '\t' +
                      self.source + '\t' +
                      self.feature_type + '\t' +
                      self.feature_start + '\t' +
                      self.feature_end + '\t' +
                      self.score + '\t' +
                      self.strand + '\t' +
                      self.phase + '\t' +
                      tmp_attribute
                      )
        return whole_line

    @property
    def seq_id(self):
        return self._seq_id

    @seq_id.setter
    def seq_id(self, value: str):
        self._seq_id = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value: str):
        self._source = value

    @property
    def feature_type(self):
        return self._feature_type

    @feature_type.setter
    def feature_type(self, value: str):
        self._feature_type = value

    @property
    def feature_start(self):
        return self._feature_start

    @feature_start.setter
    def feature_start(self, value: int):
        self._feature_start = value

    @property
    def feature_end(self):
        return self._feature_end

    @feature_end.setter
    def feature_end(self, value: int):
        self._feature_end = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: str):
        self._score = value

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, value: str):
        self._strand = value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value: str):
        self._phase = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value: list):
        self._attributes = value

    @property
    def dnaseq(self):
        return self._dnaseq

    @dnaseq.setter
    def dnaseq(self, value: str):
        self._dnaseq = value





class Organism:
    def __init__(self):

        self._strain = ""
        self._fasta = ""
        self._printable_fasta = ""
        self._gff_data = []

    def generate_feature_gtf(self, Gffdata_list):

        features = self.count_features()
        feature_keys = list(features.keys())

        feature_count = -1

        for feature in features.keys():
            feature_count += 1

            print('Generating ' + feature + '-File')
            for element in Gffdata_list:

                if not element.strain.endswith('.gtf'):
                    element.strain += '.gtf'


                filename = element.strain.strip('.gtf') + '_' + feature_keys[feature_count] + '_.gtf'

                with open(filename, 'a') as gtf_file:
                    for row in element.gff_data:
                        if row.feature_type == feature_keys[feature_count]:
                            gtf_file.write(row.get_whole_line())


    def count_features(self):

        feature_dict = {}
        for entry in self.gff_data:
            if entry.feature_type not in feature_dict.keys():
                feature_dict.update({entry.feature_type: 0})
            feature_dict[entry.feature_type] += 1

        return feature_dict


    def set_annotated_dna_seq(self, fasta_extract: bool, filename):

        if fasta_extract:
            with open(filename.replace('.gff3', '.fa'), 'w') as fasta_file:
                fasta_file.write("##sequence-region {strain}\n".format(strain=self.strain))

        for element in self.gff_data:

            if element.feature_type == 'region':
                element.dnaseq = self.fasta
                if fasta_extract:
                    with open(filename.replace('.gff3', '.fa'), 'a') as fasta_file:
                        fasta_file.write(">{idname}\n{sequence}\n".format(idname=element.attributes[0].split('=')[-1],
                                                                          sequence=self._printable_fasta))

            elif element.strand == '+':
                element.dnaseq = self.fasta[int(element.feature_start) - 1: int(element.feature_end)]

            elif element.strand == '-':
                unreverted_sequence = self.fasta[int(element.feature_start) - 1: int(element.feature_end)]
                element.dnaseq = element.get_complementary_string(sequence=unreverted_sequence)

    def print_multiple_fasta(self, data_list: list, filename: str):
        with open(filename.replace('.gff3', '.mpfa'), 'w') as file:
            for element in data_list:

                file.write("##sequence-region {strain}\n".format(strain=element.strain))

                for entry in element.gff_data[1:]:
                    file.write(">{idname}\n{sequence}\n".format(idname=entry.attributes[0].split('=')[-1],
                                                                sequence=entry.dnaseq))



    @property
    def strain(self):
        return self._strain

    @strain.setter
    def strain(self, value: str):
        self._strain = value

    @property
    def fasta(self):
        return self._fasta

    @fasta.setter
    def fasta(self, value: str):
        self._fasta = value

    @property
    def printable_fasta(self):
        return self._printable_fasta

    @printable_fasta.setter
    def printable_fasta(self, value: str):
        self._printable_fasta = value

    @property
    def gff_data(self):
        return self._gff_data

    @gff_data.setter
    def gff_data(self, value: GffData):
        self._gff_data = value
