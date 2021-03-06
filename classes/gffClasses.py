from helperfunctions import get_complementary_string


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
                element.dnaseq = get_complementary_string(sequence=unreverted_sequence)

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
    def gff_data(self, value: object):
        self._gff_data = value
