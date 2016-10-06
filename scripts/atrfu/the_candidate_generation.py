import requests
import urllib.request
import urllib
import os
import subprocess
import ast
import pickle
import operator

def obtain_view(entity, date, debug=False):
    """

    >>> obtain_view('France', '2015-07-01')
    8920

    """
    result = 0

    for element, replace in [('(', '\('),
                             (')', '\)'),
                             ('&', '\&'),
                             ("'", "")]:
        entity = entity.replace(element, replace)

    date_for_command = date.replace('-', '')
    command = 'node get_views.js {entity} {date_for_command} {date_for_command}'.format(
        **locals())

    try:
        output = subprocess.check_output(command, shell=True)
        output = output.decode('utf-8')
        views = ast.literal_eval(output)
    except subprocess.CalledProcessError:
        print('ERROR', command)
        views = {}

    if date in views:
        result = sum(views.values())

    if debug:
        print()
        print(command)
        print(result)
        input('continue?')

    return result


def get_dbpedia_results(query, debug=False):
    if debug:
        print(query)
    q = {'query': query, 'format': 'json'}
    s = 'http://dbpedia.org/sparql'
    url = s + '?' + urllib.parse.urlencode(q)
    if debug:
        print()
        print(url)
    r = requests.get(url=url)
    if r.status_code == 200:
        page = r.json()
        results = {result['link']['value']
                   for result in page["results"]["bindings"]}
    else:
        results = set()
    return results


def candidates_to_freq(goldmention, goldlink, date, debug=False):
    """
    """
    freq = {}
    query = '''select distinct(?link) where { ?disambiguation rdfs:label ?lbl. FILTER (STR(?lbl) in ("%s", "%s (disambiguation)")) . ?disambiguation <http://dbpedia.org/ontology/wikiPageDisambiguates> <%s> , ?link .}''' % (goldmention, goldmention, goldlink)
    candidates = get_dbpedia_results(query, debug=False)
    in_candidates = goldlink in candidates

    if not in_candidates:
        return {}


    if candidates:
        if debug:
            print()
            print(goldmention, goldlink)
            print(goldlink + '_(disambiguation)')
            print(candidates)

        for candidate in candidates:

            entity = candidate.replace('http://dbpedia.org/resource/', '')
            view_count = obtain_view(entity, date, debug=False)

            freq[candidate] = view_count

            if debug:
                print('CANDIDATE', entity, view_count)

        if debug:
            input('continue?')

    return freq


def get_rank_and_relfreq(key, d, debug=False):
    """
    given a dictionary mapping keys to values
    this function returns the rank of the key and the relfreq
    """
    if key not in d:
        return (False, None, None)

    total = sum(d.values())
    if total == 0:
        return (False, None, None)

    sorted_d = [link
                for link, value in sorted(d.items(),
                                          key=operator.itemgetter(1),
                                          reverse=True)]
    rank = sorted_d.index(key) + 1
    rel_freq = 100 * (d[key] / sum(d.values()))

    if debug:
        print()
        print(key)

        for link, value in sorted(d.items(),
                                  key=operator.itemgetter(1),
                                  reverse=True):
            print(link, value)
        print(rank, rel_freq)
        input('continue?')
    return (True, rank, rel_freq)


def compute_entity_ranks_relfreqs(iterable, cache_path, fixed_date=None):
    """
    loop over iterable

    :param iterable: iterable of tuples (identifier, goldmention, goldlink, date)
    date is of format yyyy-mm-dd
    :param str cache_path: path where cache (pickled dict) will be stored
    :param datetime.datetime fixed_date: if not None, this date will be used to compute the
    entity rank and relative frequencies

    :rtype: tuple
    :return: cache, avg_rank, avg_relfreq
    """
    all_ranks = []
    all_relfreqs = []

    if os.path.exists(cache_path):
        cache = pickle.load(open(cache_path, 'rb'))
    else:
        cache = {}

    total = len(iterable)
    for counter, (identifier, goldmention, goldlink, date) in enumerate(
            iterable):
        if fixed_date is not None:
            date = fixed_date

        if identifier in cache:
            freq = cache[identifier]
        else:
            freq = candidates_to_freq(goldmention, goldlink, date,
                                      debug=False)
            cache[identifier] = freq

        if freq:
            succes, rank, relfreq = get_rank_and_relfreq(goldlink, freq,
                                                         debug=False)
            if succes:
                all_ranks.append(rank)
                all_relfreqs.append(relfreq)

        print(counter, total, goldmention, goldlink)
        with open(cache_path, 'wb') as outfile:
            pickle.dump(cache, outfile)

    avg_rank = sum(all_ranks) / len(all_ranks)
    avg_relfreq = sum(all_relfreqs) / len(all_relfreqs)

    return cache, avg_rank, avg_relfreq