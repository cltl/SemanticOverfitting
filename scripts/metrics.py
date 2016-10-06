import datetime
from math import *

def MOA(o_l):
    '''
    Mean Observed Ambiguity (MOA)

    >>> MOA({'horse' : set(['horse.n.1','horse.n.2']),'house': set(['house.n.1'])})
    1.5
    >>> MOA({})
    0.0

    We define observed ambiguity of an expression as the cardinality of the set of meanings it refers to within a dataset (:math:`O_{L_i}`).
    The MOA of a dataset is the average of the individual observed ambiguity values.

    :param dict o_l: dict mapping lexical expressions to length of set of observed meanings

    :rtype: float
    :return: Mean Observed Ambiguity (MOA)
    '''
    if o_l:
        observed_ambiguities = [len(value) for value in o_l.values()
                                if value]
        moa = sum(observed_ambiguities)/len(observed_ambiguities)
    else:
        moa = 0.0

    return moa

def MOV(o_m):
    '''
    Mean Observed Variance (MOV)

    >>> MOV({'car.n.1' : set(['car','automobile']),'house.n.1': set(['house','mansion'])})
    2.0
    >>> MOV({})
    0.0

    We define observed variance of a meaning as the cardinality of the set of lexical expressions that express it within a dataset (:math:`O_{M_j}`).
    The MOV of a dataset is the average of the individual observed variance values.

    :param dict o_m: dict mapping meanings to length of set of observed lexical expressions

    :rtype: float
    :return: Mean Observed Variance (MOV)
    '''
    if o_m:
        observed_variances = [len(value) for value in o_m.values()
                              if value]
        mov = sum(observed_variances)/len(observed_variances)
    else:
        mov = 0.0

    return mov

def MODA(amb_dominance_distribution):
    '''
    Mean Observed Dominance of Ambiguity (MODA)

    We define dominance of ambiguity as a frequency distribution of the dominant meaning of a lexical expression.
    The MODA of a dataset is the average dominance of all observed expressions.

    >>> MODA([0.5,0.6,0.7])
    0.6

    >>> MODA([])
    0.0

    :param list amb_dominance_distribution: list containing the percentages for each dominant meaning of a lexical expression as observed in a dataset

    :rtype: float
    :return: Mean Observed Dominance of Ambiguity (MODA)
    '''
    if amb_dominance_distribution:
        dominances = [value for value in amb_dominance_distribution
                      if value]
        moda = sum(dominances)/len(dominances)
    else:
        moda = 0.0

    return moda

def MODV(var_dominance_distribution):
    '''
    Mean Observed Dominance of Variance (MODV)

    >>> MODV([0.4,0.6,0.8])
    0.6

    >>> MODV([])
    0.0

    We define the notion of dominance of variance, as a frequency distribution of the dominant lexical expression referring to a meaning.
    The MODV of a dataset is then the average dominance computed over all observed meanings.

    :param list var_dominance_distribution: list containing the percentages for each dominant lexical expression of a meaning as observed within a dataset

    :rtype: float
    :return: Mean Observed Dominance of Variance (MODV)
    '''
    if var_dominance_distribution:
        dominances = [value for value in var_dominance_distribution
                      if value]
        modv = sum(dominances)/len(dominances)
    else:
        modv = 0.0

    return modv

def EMNLE(list_of_entropy_values):
    '''
    Entropy of the Meanings (Normalized) of a Lexical Expression

    .. math::
	   EMNLE(O_L,R_L) = \\frac{1}{n} \\sum\\limits_{i=1}^n H(O_{L_i},R_{L_i})

    :param list list_of_entropy_values: list of entropy values
    >>> EMNLE([0.5,0.5,0.2])
    0.4

    >>> EMNLE([0.0,0.0,0.0,1.0])
    0.25

    :rtype: float
    :return: average entropy of ambiguity
    '''
    return sum(list_of_entropy_values)/len(list_of_entropy_values)

def ELENM(list_of_entropy_values):
    '''
    Entropy of the Lexical Expressions (Normalized) of a Meaning

    .. math::
	   ELENM(O_M,R_M) = \\frac{1}{n} \\sum\\limits_{j=1}^n H(O_{M_j},R_{M_j})

    :param list list_of_entropy_values: list of entropy values
    >>> ELENM([0.5,0.5,0.2])
    0.4

    >>> ELENM([0.0,0.0,0.0,1.0])
    0.25

    :rtype: float
    :return: average entropy of variance
    '''
    return sum(list_of_entropy_values)/len(list_of_entropy_values)

def RORA(o_l, r_l, ignore_theoretical_one=True):
    '''
    Ratio between observed and resource ambiguity


    >>> RORA({'horse' : len(set(['horse.n.1','horse.n.2'])),'house': len(set(['house.n.1']))}, {'horse' : len(set(['horse.n.1','horse.n.2','horse.n.3','horse.n.4'])),'house': len(set(['house.n.1','house.n.2']))})
    0.5

    .. math::
        RORA(O_L,R_L) = \\frac{1}{n} \\sum\\limits_{i=1}^n ratio_{amb}(O_{L_i},R_{L_i})

    :param dict o_l: dict mapping lexical expressions to length of set of observed meanings
    :param dict r_l: dict mapping lexical expressions to length of set of resource meanings
    :param ignore_theoretical_one: boolean value which indicates whether the monosemous cases should be ignored. We set this to True in our Analysis (Section 5).
    '''
    ambiguities = []

    for le,o_l_i in o_l.items():

        # if no o_l_i
        if not o_l_i:
            continue

        # if no r_l_i
        if le not in r_l:
            continue

        r_l_i = r_l[le]
        if not r_l_i:
            continue


        if all([ignore_theoretical_one,
                r_l_i == 1]):
            continue

        amb = ambiguity(o_l_i,r_l_i)
        ambiguities.append(amb)

    rora_value = (1.0/len(ambiguities)) * sum(ambiguities)

    return rora_value

def RORV(o_m, r_m, ignore_theoretical_one=True):
    '''
    Ratio between observed and resource variance

    .. math::
        RORV(O_M,R_M) = \\frac{1}{n} \\sum\\limits_{i=1}^n ratio_{var}(O_{M_j},R_{M_j})

    >>> RORV({'car.n.1' : len(set(['car','automobile'])),'house.n.1': len(set(['house','mansion']))},{'car.n.1' : len(set(['car','automobile','vehicle','wagon'])),'house.n.1': len(set(['house','mansion','shack','residence']))})
    0.5

    :param dict o_m: dict mapping meanings to length of set of observed lexical expressions
    :param dict r_m: dict mapping meanings to length of set of resource lexical expressions

    :rtype: float
    :return: Ratio between observed and resource variance on a dataset level
    '''
    variances = []

    for m,o_m_j in o_m.items():

        #log if no o_m_j
        if not o_m_j:
            continue

        #log if no r_m
        if m not in r_m:
            continue

        r_m_j = r_m[m]

        if not r_m_j:
            continue

        if all([ignore_theoretical_one,
                r_m_j == 1]):
            continue

        var = variance(o_m_j,r_m_j)
        variances.append(var)

    if variances:
        rorv_value = (1.0/len(variances)) * sum(variances)
    else:
        rorv_value = 0.0

    return rorv_value


def ambiguity(o_l_i,r_l_i):
    '''
    Ratio between observed and resource ambiguity for a single lexical expression

    >>> ambiguity(len(set(['bank.n.1'])), len(set(['bank.n.1','bank.n.2'])))
    0.5

    .. math::
        ratio_{amb}(O_{L_i},R_{L_i})  = \\frac{|\{M_j:M_j \\in O_{L_i}\}|}{|\{M_j:M_j \\in R_{L_i}\}|}

    :param int o_l_i: length of set of observed meanings for lexical expression
    :param int r_l_i: length of set of resource meanings for lexical expression

    :rtype: float
    :return: ratio between observed and resource ambiguity
    '''
    return o_l_i/r_l_i


def variance(o_m_j,r_m_j):
    '''
    Ratio between observed and resource variance for a single meaning

    .. math:: ratio_{var}(O_{M_j},R_{M_j})  = \\frac{|\{L_i:L_i \\in O_{M_j}\}|}{|\{L_i:L_i \\in R_{M_j}\}|}

    >>> variance(1,2)
    0.5

    :param int o_m_j: length of set of lexical expressions which can verbalize a certain meaning
    :param int r_m_j: length of set of lexical expressions that express a meaning as observed within a dataset

    :rtype: float
    :return: ratio between observed and resource variance
    '''
    return o_m_j/r_m_j

def entropy(list_of_probs,
            normalized=False,
            base=2):
    '''
    Entropy for a lexical expression/meaning, consequently, computed according to the formulas\:

    .. math::
        H(O_{L_i}) = \\frac{ -\\sum\\limits_{j=1}^n p(M_j|L_i) log_2p(M_j|L_i) } {log_2(n)}

        H(O_{M_j}) = \\frac{ -\\sum\\limits_{i=1}^n p(L_i|M_j) log_2p(L_i|M_j) } {log_2(n)}

    >>> entropy([0.2,0.2,0.2,0.2,0.2],normalized=True)
    1.0

    >>> entropy([0.2,0.2,0.2,0.2,0.2],normalized=False)
    2.321928094887362

    >>> entropy([])
    0.0

    :param list list_of_probs: list of probabilities
    :param bool normalized: True: normalized entropy will be returned
    :param int base: log base

    :rtype: float
    :return: normalized entropy. 0.0 is returned if list is empty
    '''
    #if empty list, return 0.0:
    if not list_of_probs:
        return 0.0

    #calculate Shannon Entropy (S) = -Si(piLnpi)
    S = -1.0 * sum([ (p * ( log(p,base) ) )
                  for p in list_of_probs])

    #normalize if needed
    if all([normalized,
           len(list_of_probs) >= 2]):
        len_list_of_probs = len(list_of_probs)
        S = S/log(len_list_of_probs,base)

    return abs(S)

def DTR(dates):
    '''
    Dataset Time Range -> time interval between the earliest and the latest published document of a dataset

    .. math::

        DTR = min(date_{doc}), max(date_{doc})

    where :math:`date_{doc}` is the publishing date of a document.

    :param list dates: list of dates (e.g. '2015-1-26')

    >>> DTR(['2015-1-28','2015-1-26', '2013-8-12', '2014-3-2'])
    [datetime.datetime(2013, 8, 12, 0, 0), datetime.datetime(2015, 1, 28, 0, 0)]

    :rtype: list
    :return: list of two datetime values, denoting the earliest and the latest document publishing date
    '''
    dates_in_format =[datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]
    return [min(dates_in_format), max(dates_in_format)]
