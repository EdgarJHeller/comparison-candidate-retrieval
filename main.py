import query_sentences
import extract_candidates
import filter_candidates_wordnet
import filter_candidates_classifier
import filter_candidates_DT
import query_DT_candidates
import object_lists
import csv


def get_percent_contained(comparison_object, selected_candidates):
    evaluation_candidates = object_lists.evaluation_lists[comparison_object]
    intersection = list(
        set(evaluation_candidates).intersection(selected_candidates))

    return len(intersection) / len(evaluation_candidates)


if __name__ == "__main__":
    with open('./results/evaluation.csv', 'a', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows([['whithout', 'wordnet', 'classifier', 'DT']])

    for comparison_object in object_lists.objects:

        # sentences = query_sentences.retrieve_sentences(comparison_object)
        # candidates = extract_candidates.extract_candidates(comparison_object, sentences)

        candidates = query_DT_candidates.get_all_similarities(comparison_object)

        first_ten_candidates = candidates#[c[0] for c in candidates]
        wordnet_filtered_candidates = [] #filter_candidates_wordnet.filter(comparison_object, candicates)
        classifier_filtered_candidates = [] #filter_candidates_classifier.filter(comparison_object, candicates)
        DT_filtered_candidates = [] #filter_candidates_DT.filter(comparison_object, candicates)

        print('---------', comparison_object ,'---------')
        # print(first_ten_candidates)
        print(wordnet_filtered_candidates)
        print(classifier_filtered_candidates)
        print(DT_filtered_candidates)
        


        with open('./results/candidates.csv', 'a', newline='', encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerows([first_ten_candidates, wordnet_filtered_candidates,
                    classifier_filtered_candidates, DT_filtered_candidates])

        results = [[get_percent_contained(comparison_object, first_ten_candidates),
                    get_percent_contained(
                        comparison_object, wordnet_filtered_candidates),
                    get_percent_contained(
                        comparison_object, classifier_filtered_candidates),
                    get_percent_contained(comparison_object, DT_filtered_candidates)]]

        with open('./results/evaluation.csv', 'a', newline='', encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerows(results)

