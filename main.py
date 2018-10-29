import query_sentences
import extract_candidates
import filter_candidates_wordnet
import filter_candidates_classifier


if __name__ == "__main__":

    comparison_object = 'python'
    sentences = query_sentences.retrieve_sentences(comparison_object)
    candicates = extract_candidates.extract_candidates(
        comparison_object, sentences)
    print('Candidates: ')
    print(candicates)
    # filtered_candidates = filter_candidates_wordnet.filter_candidates_wordnet(comparison_object, candicates)
    filtered_candidates = filter_candidates_classifier.filter(
        comparison_object, candicates)

    print(filtered_candidates)
    print('-----------------')
    result = [candidate[0][0] for candidate in filtered_candidates]
    print(result)
    # print(filtered_candidates)

