from nltk.corpus import wordnet as wn
import queue



def filter_candidates_wordnet(comparison_object, candidates):
    hypernyms_comparison_object = get_all_hypernyms(comparison_object)
    print(hypernyms_comparison_object)
    filtered_candidates = []
    for candidate in candidates:
        print('---', candidate, '---')

        candidate_hypernyms = get_all_hypernyms(candidate[0])
        print(candidate_hypernyms)
        if not set(hypernyms_comparison_object).isdisjoint(candidate_hypernyms):
            filtered_candidates.append(candidate)

    return filtered_candidates



def get_all_hypernyms(comparison_object):
    q = queue.Queue()

    for ss in wn.synsets(comparison_object):
        for hypernym in ss.hypernyms():
            q.put(hypernym)

    hypernyms = []
    while not q.empty():
        hypernym = q.get()
        hypernyms.append(hypernym)
        for hypernym in hypernym.hypernyms():
            q.put(hypernym)

    return hypernyms