class MastFile(object):
    """A class for mast files.

    Extension of Bio.motifs.mast.Record
    """

    def __init__(self, record):
        """Takes a Bio.motifs.mast.Record object as parameter."""
        self.sequences = [MastSequence(sequence_name, motif_diagram)
                          for sequence_name, motif_diagram
                          in record.diagrams.iteritems()]


class MastSequence(object):
    """A class for mast sequences in SECTION II

    Attributes
    ----------
    name : sequence name column
    organism : organism mnenomic ID from self.name
    diagram : motif diagram column
    gene_classification : 'MDM2'/'Corp'/'Other'
    """

    def __init__(self, name, diagram_string):
        self.name = name
        self.organism = name[name.find('_') + 1:]
        self.diagram = Diagram(diagram_string)
        self.gene_classification = None
        self.__classify_like_gene()

    def __classify_like_gene(self):
        """Classify as MDM2 or Corp based on self.diagram"""
        if (self.diagram.has_motif(1) and
                self.diagram.has_motif(2) and
                self.diagram.has_motif(3)):
            self.gene_classification = 'MDM2'
        elif (self.diagram.has_motif(1) and
              not self.diagram.has_motif(2) and
              not self.diagram.has_motif(3)):
            self.gene_classification = 'Corp'
        else:
            self.gene_classification = 'Other'

    def __repr__(self):
        return ('MastSequence(organism="{0.organism}",'
                'diagram="{0.diagram}")'.format(self))


class Diagram():
    """A class for motif diagrams

    Attributes
    ----------
    string : diagram string (from SECTION II)
    motifs : list of DiagramMotif
    """

    def __init__(self, diagram_string):
        self.string = diagram_string
        self.motifs = []
        self.__parse_string()

    def __parse_string(self):
        """Parse self.string"""
        self.list = self.string.split('_')
        for i, part in enumerate(self.list):
            try:
                self.list[i] = int(part)
            except ValueError:
                motif = DiagramMotif(int(part[1:-1]))
                self.list[i] = motif
                self.motifs.append(motif)

    def has_motif(self, motif_num):
        return any([motif_num is motif.num
                    for motif in self.motifs])

    def __str__(self):
        return self.string


class DiagramMotif():
    """A class for basic diagram motifs"""

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return 'Motif(num={!r})'.format(self.num)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        """Equality based on class attributes"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Non-equality"""
        return not self.__eq__(other)

    def __hash__(self):
        """Hash class attributes rather than id"""
        return hash(tuple(sorted(self.__dict__.items())))
