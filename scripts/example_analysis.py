import sys
import json
import metrics as metrics

def compute_ambiguity_metrics(mentions_to_links, l, data_totals, resource_totals):
    """
    This function computes all ambiguity metrics: MOA, EMNLE and MODA. The ratio between resource and dataset ambiguity, RORA, could also be computed, provided that one has the dataset loaded locally.
    """
    o_l={}
    e=[]
    amb_dominance_distribution=[]
    uniq_totals={}
    for sf in mentions_to_links:
        total=data_totals[sf]
        entropy=[]
        for link in mentions_to_links[sf]:
            entropy.append(mentions_to_links[sf][link]*1./total)
        e.append(metrics.entropy(entropy, True))
        amb_dominance_distribution.append(max(entropy))
        
        o_l[sf]=set(mentions_to_links[sf])
        uniq_totals[sf]=len(o_l[sf])

    print("Ambiguity metrics:")
    print("MOA: ",metrics.MOA(o_l))
    print("EMNLE: ", metrics.EMNLE(e))
    print("MODA: ", metrics.MODA(amb_dominance_distribution))
    if len(resource_totals):
        print("RORA: ", metrics.RORA(uniq_totals, resource_totals, True))

def compute_variance_metrics(links_to_mentions, l, data_totals, resource_totals):
    """
    This function computes all variance metrics: MOV, ELENM and MODV. The ratio between resource and dataset variance, RORV, could also be computed, provided that one has the dataset loaded locally.
    """

    # Compute ROTV
    e=[]
    o_m={}
    var_dominance_distribution=[]
    uniq_totals={}
    for link in links_to_mentions:
        total=data_totals[link]
        entropy=[]
        for sf in links_to_mentions[link]:
            entropy.append(links_to_mentions[link][sf]*1./total)
        e.append(metrics.entropy(entropy, True))
        var_dominance_distribution.append(max(entropy))
        o_m[link]=set(links_to_mentions[link])
        uniq_totals[link]=len(o_m[link])    

    print("Variance metrics:")
    print("MOV: ",metrics.MOV(o_m))
    print("ELENM: ",metrics.ELENM(e))
    print("MODV: ", metrics.MODV(var_dominance_distribution))
    if len(resource_totals):
        print("RORV: ", metrics.RORV(uniq_totals, resource_totals, True))

def extract_jsons(filename):
    """
    This function creates two json structures: 1) JSON which counts and groups the meanings of a LE, and 2) JSON which counts and groups the LEs for a meaning.
    """
    sf_to_links={}
    links_to_sf={}
    sf_data_totals={}
    sf_resource_totals={}
    links_data_totals={}
    links_resource_totals={}
    o_l={}
    o_m={}
    dates=[]
    single_sf=0
    with open(filename,'r') as tsvin:
        for line in tsvin:
            row=line.strip().split('\t')
            if len(row)==6:
                    # FOR AMBIGUITY
                    if row[1] not in sf_to_links:
                        sf_to_links[row[1]]={row[2]:1}
                    elif row[2] in sf_to_links[row[1]]:
                        sf_to_links[row[1]][row[2]]+=1
                    else:
                        sf_to_links[row[1]][row[2]]=1
                    if row[1] not in sf_data_totals:
                        sf_data_totals[row[1]]=1
                    else:
                        sf_data_totals[row[1]]+=1
                    if row[4].lower()!="none":
                        sf_resource_totals[row[1]]=int(row[4])
                    
                    # FOR VARIANCE
                    if row[2] not in links_to_sf:
                        links_to_sf[row[2]]={row[1]:1}
                    elif row[1] in links_to_sf[row[2]]:
                        links_to_sf[row[2]][row[1]]+=1
                    else:
                        links_to_sf[row[2]][row[1]]=1
                    if row[2] not in links_data_totals:
                        links_data_totals[row[2]]=1
                    else:
                        links_data_totals[row[2]]+=1
                    if row[5].lower()!="none":
                        links_resource_totals[row[2]]=int(row[5])

                    if row[3].lower()!="none":
                        dates.append(row[3])

    return sf_to_links, links_to_sf, sf_data_totals, links_data_totals, sf_resource_totals, links_resource_totals, dates

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Please add the TSV file of the dataset as an argument")
        print("Usage: python example_analysis.py dataset.tsv")
        sys.exit(1)
    
    
    sf_to_links, links_to_sf, sf_data_totals, links_data_totals, sf_resource_totals, links_resource_totals, dates=extract_jsons(sys.argv[1])

    print(sf_to_links)

    compute_ambiguity_metrics(sf_to_links, len(links_to_sf), sf_data_totals, sf_resource_totals)
    compute_variance_metrics(links_to_sf, len(sf_to_links), links_data_totals, links_resource_totals)
    if len(dates):
        DTR=metrics.DTR(dates)
        print("DTR:")
        print(DTR)

