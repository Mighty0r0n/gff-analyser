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


class Organism:
    def __init__(self):
        self._strain = ""
        self._fasta = ""
        self._gff_data = []

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
    def gff_data(self):
        return self._gff_data

    @gff_data.setter
    def gff_data(self, value: str):
        self._gff_data = value
