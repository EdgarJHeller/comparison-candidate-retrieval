import query_sentences
import extract_candidates
import filter_candidates_wordnet
import filter_candidates_classifier
import filter_candidates_DT
import query_DT_candidates
import object_lists
import csv


CANDIDATES_CSV_PATH = './results/candidates.csv'
EVALUATION_CSV_PATH = './results/evaluation.csv'

def get_percent_contained(comparison_object, selected_candidates):
    evaluation_candidates = object_lists.evaluation_lists[comparison_object]
    intersection = list(
        set(evaluation_candidates).intersection(selected_candidates))

    return len(intersection) / len(evaluation_candidates)


if __name__ == "__main__":
    with open(EVALUATION_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows([['whithout', 'wordnet', 'classifier', 'DT']])
    
    with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows([['Comparison Object:', 'Candidates:']])

    for comparison_object in object_lists.preSelectedObjects:

        sentences = query_sentences.retrieve_sentences(comparison_object)
        candidates = extract_candidates.extract_candidates(comparison_object, sentences)

        wordnet_filtered_candidates = filter_candidates_wordnet.filter(comparison_object, candidates)

        print('---------', comparison_object ,'---------')
        print(first_ten_candidates)
        print(wordnet_filtered_candidates)
        print(classifier_filtered_candidates)
        print(DT_filtered_candidates)
        


        with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
            writer = csv.writer(f)
            if not wordnet_filtered_candidates:
                writer.writerows([[comparison_object]])
            else:
                writer.writerow([comparison_object] + wordnet_filtered_candidates)


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
