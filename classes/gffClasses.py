
class GffData:
    def __init__(self, seq_id):
        self.seq_id = seq_id[0]
        self.source = seq_id[1]
        self.feature_type = seq_id[2]
        self.feature_start = seq_id[3]
        self.feature_end = seq_id[4]
        self.score = seq_id[5]
        self.strand = seq_id[6]
        self.phase = seq_id[7]
        self.attributes = seq_id[8].split(";")


class Bacteria:
    def __init__(self):
        self._region = ""
        self._fasta = ""
        self.gff_data = []

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value: str):
        self._region = value

    @property
    def fasta(self):
        return self._fasta

    @fasta.setter
    def fasta(self, value: str):
        self._fasta = value

