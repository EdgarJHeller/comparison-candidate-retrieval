import query_sentences
import extract_candidates
import filter_candidates_wordnet
import filter_candidates_classifier
import filter_candidates_DT
import query_DT_candidates
import object_lists
import csv
import sys
import calculate_levenshtein_distance
import query_ggl_suggestions


CANDIDATES_CSV_PATH = './results/candidates.csv'
EVALUATION_CSV_PATH = './results/evaluation.csv'

def get_percent_contained(comparison_object, selected_candidates):
    evaluation_candidates = object_lists.evaluation_lists[comparison_object]
    intersection = list(
        set(evaluation_candidates).intersection(selected_candidates))

    return len(intersection) / len(evaluation_candidates)


if __name__ == "__main__":
    # write headlines to evaluation csv
    with open(EVALUATION_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows([['whithout', 'wordnet', 'classifier', 'DT']])
    
    # write headlines to candidates csv
    with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows([['Comparison Object:', 'Candidates:']])

    # the comparison object is now set as third parameter when main is called
    # eg: python main.py reader reader python -> comparison object is "python"
    comparison_object = sys.argv[3]
    
    # sentences is a list with sentenses that contain the comparison_object AND vs
    sentences = query_sentences.retrieve_sentences(comparison_object)
    candidates = extract_candidates.extract_candidates(comparison_object, sentences)

    wordnet_filtered_candidates = filter_candidates_wordnet.filter(comparison_object, candidates)

    print('---------', comparison_object ,'---------')
    print(wordnet_filtered_candidates)
    
    # the suggestions as a list of lists
    ggl_suggestions = query_ggl_suggestions.get_suggestions(comparison_object + ' vs')
    # the suggestions of a list of strings
    ggl_suggestions = [item[0] for item in ggl_suggestions]
    # each suggestions stripped of the comparison object and the 'vs'
    ggl_suggestions = [s[len(comparison_object + ' vs '): ] for s in ggl_suggestions]
    
    dist_matrix = calculate_levenshtein_distance.get_distance_matrix(ggl_suggestions, wordnet_filtered_candidates)
    levenshtein_distance_minima = dist_matrix.min(1)
    print(levenshtein_distance_minima)
    print(levenshtein_distance_minima.sum())
    



    with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        if not wordnet_filtered_candidates:
            writer.writerows([[comparison_object]])
        else:
            writer.writerow(['ccr'] + [comparison_object] + wordnet_filtered_candidates)
            writer.writerow(['ggl'] + [comparison_object] + ggl_suggestions)


'''
        results = [[get_percent_contained(
                        comparison_object, first_ten_candidates),
                    get_percent_contained(
                        comparison_object, wordnet_filtered_candidates),
                    get_percent_contained(
                        comparison_object, classifier_filtered_candidates),
                    get_percent_contained(comparison_object, DT_filtered_candidates)]]

        with open(EVALUATION_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerows(results)
'''
