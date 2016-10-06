import metrics
from collections import defaultdict
from collections import Counter


class Analysis:

    
    def __init__(self, corpus_path):
        self.le2m, self.m2le = self.load(corpus_path)
        self.create_input_formats()

        self.moa = metrics.MOA(self.o_l)
        self.moda = metrics.MODA(self.amb_dominance)
        self.emnle = metrics.EMNLE(self.amb_dominance)
        self.dtr = metrics.DTR(self.dates)

        self.rora = 0.0
        if self.ra:
            self.rora = metrics.RORA(self.oa, self.ra)

        self.mov = metrics.MOV(self.o_m)
        self.modv = metrics.MODV(self.var_dominance)
        self.elenm = metrics.ELENM(self.var_entropy)

        self.rorv = 0.0
        if self.rorv:
            self.rorv = metrics.RORV(self.ov, self.rv)

    def load(self, corpus_path):
        """
        load mappings:
        lexical expression -> meanings
        meanings -> lexical expressions

        :param str corpus_path: path to corpus in tsv format
        1. identifier
        2. lexical expression
        3. meaning
        4. [if available] document creation time
        5. [if available] resource ambiguity
        6. [if available] resource variance


        :rtype: tuple
        :return: (lexical expression -> meaning,
                  meaning -> lexical expression
        """
        le2m = defaultdict(list)
        m2le = defaultdict(list)
        self.ra = {}
        self.rv = {}
        self.dates=set()
        with open('../datasets/' + corpus_path) as infile:
            for line in infile:

                try:
                    iden, le, m, dct, r_amb, r_var = line.strip().split('\t')
                except ValueError:
                    continue

                if dct.strip() not in {'NONE', 'None', ''}:
                    self.dates.add(dct)
                if r_amb not in {'NONE', 'None'}:
                    r_amb = int(r_amb)
                    self.ra[le] = r_amb
                if r_var not in {'NONE', 'None'}:
                    r_var = int(r_var)
                    self.rv[m] = r_var

                le2m[le].append(m)
                m2le[m].append(le)

        return le2m, m2le

    def get_distribution(self, a_list):
        """
        compute probability of each item in the list

        :param a_list: a list of items

        :rtype: list
        :return: list of probabilities of each item
        """
        counts = Counter(a_list)
        total = len(a_list)

        distribution = []

        for item, freq in counts.items():
            rel_freq = freq / total
            distribution.append(rel_freq)

        return distribution

    def create_input_formats(self):
        """
        each metric requires the data in a certain format this method
        prepares those
        """
        # moa: m -> set([le1, le2])
        self.o_m = {}
        # moda: list of dominant percentages
        self.amb_dominance = []
        # emnle: list of entropy values (meaning distribution)
        self.amb_entropy = []

        # rora:
            # (oa) le -> int (observed ambiguity))
            # (ra) le -> int (resource ambiguity)
        self.oa = {}

        # mov l -> set([m1, m2])
        self.o_l = {}
        # modv: list of dominant percentages
        self.var_dominance = []
        # elenm: list of entropy values (le distribution)
        self.var_entropy = []
        # rora:
            # le -> int (observed ambiguity))
            # le -> int (resource ambiguity)
        self.ov = {}

        for le, meanings in self.le2m.items():
            self.o_l[le] = set(meanings)

            self.oa[le] = len(set(meanings))

            distribution = self.get_distribution(meanings)
            maximum = max(distribution)
            entropy = metrics.entropy(distribution, normalized=True)

            self.amb_dominance.append(maximum)
            self.amb_entropy.append(entropy)

        for m, les in self.m2le.items():
            self.o_m[m] = set(les)

            self.ov[m] = len(set(les))

            distribution = self.get_distribution(les)
            maximum = max(distribution)
            entropy = metrics.entropy(distribution, normalized=True)

            self.var_dominance.append(maximum)
            self.var_entropy.append(entropy)
