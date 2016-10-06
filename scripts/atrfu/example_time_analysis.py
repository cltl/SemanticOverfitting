from datetime import datetime
from the_candidate_generation import compute_entity_ranks_relfreqs
from lxml import etree
import os
from glob import glob
import pickle


def get_wid2w(doc):
    """
    """
    wid2w = {wf_el.get('id'): wf_el.text
             for wf_el in doc.xpath('text/wf')}
    return wid2w

def get_mention2goldlink(input_path, debug=False):
    """
    """
    mention2goldlink = {}
    doc = etree.parse(input_path)
    wid2w = get_wid2w(doc)

    for entity_el in doc.xpath('entities/entity'):

        # entity id
        entity_id = entity_el.get('id')

        # get gold link
        ext_ref_el = entity_el.find('externalReferences/externalRef')
        if ext_ref_el is None:
            continue

        goldlink = ext_ref_el.get('reference')
        if goldlink in {'None', None}:
            continue

        # mentions
        wids = [target_el.get('id')
                for target_el in entity_el.xpath('references/span/target')]
        if not wids:
            continue

        mention = ' '.join([wid2w[wid] for wid in wids])
        goldlink = goldlink.replace('http://dbpedia.org/page',
                                    'http://dbpedia.org/resource')
        mention2goldlink[(entity_id, mention)] = (goldlink, wids)

        if debug:
            print()
            print(entity_id, mention)
            print(wids)
            etree.dump(entity_el)
            input('continue?')

    return mention2goldlink

# create iterable for meantime corpus
views_from = datetime(2007, 12, 1)

filename='meantime_with_times.tsv'

cache_path = 'cache.pickle'
iterable = []
with open(filename, 'r') as f:
    for line in f:
        line=line.split('\t')
        goldmention=line[0]
        goldlink=line[1]
        creation_time=line[2]
        identifier=line[3]
        print(line)
        print(creation_time)
        year, month, day = creation_time.split('-')
        ct_datetime = datetime(int(year), int(month), int(day))
        if ct_datetime < views_from:
            continue

        iterable.append((identifier, goldmention, goldlink, creation_time))

# run it on the meantime corpus
run = True
if run:
    mt_cache, mt_avg_rank, mt_avg_relfreq = compute_entity_ranks_relfreqs(iterable, 'meantime.pickle')
    print()
    print('meantime.pickle')
    print(round(mt_avg_rank,2), round(mt_avg_relfreq,2))
    mt_cache, mt_avg_rank, mt_avg_relfreq = compute_entity_ranks_relfreqs(iterable,
                                                                          'meantime2007-12.pickle',
                                                                          datetime(2007, 12, 1))
    print()
    print('meantime2007-12.pickle')
    print(round(mt_avg_rank,2), round(mt_avg_relfreq,2))
    mt_cache, mt_avg_rank, mt_avg_relfreq = compute_entity_ranks_relfreqs(iterable,
                                                                          'meantime2011-12.pickle',
                                                                          datetime(2011, 12, 1))
    print()
    print('meantime2011-12.pickle')
    print(round(mt_avg_rank,2), round(mt_avg_relfreq,2))
    mt_cache, mt_avg_rank, mt_avg_relfreq = compute_entity_ranks_relfreqs(iterable,
                                                                          'meantime2015-12.pickle',
                                                                          datetime(2015, 12, 1))
    print()
    print('meantime2015-12.pickle')
    print(round(mt_avg_rank,2), round(mt_avg_relfreq,2))
