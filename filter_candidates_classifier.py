from nltk.corpus import wordnet as wn
import query_sentences
from pandas import DataFrame
import re
import operator
from cam_pretrained.model_util import load_model


def filter(comparison_object, candidates):

    filtered_candidates = []
    for candidate in candidates:
        print('Start query sentences of', comparison_object, 'and', candidate)
        sentences = query_sentences.retrieve_sentences(comparison_object, candidate[0])
        print('Start classifying the', len(sentences),'sentences...')
        classification_result = classify_sentences(prepare_sentence_DF(sentences, comparison_object, candidate[0]))

        classification_result = classification_result[classification_result['max'] != 'NONE']

        print(len(classification_result))
        if len(classification_result) > 40:
            filtered_candidates.append((candidate, len(classification_result)))

    filtered_candidates = [(candidate[0][0], candidate[1]*candidate[0][1]) for candidate in filtered_candidates]
    filtered_candidates = sorted(filtered_candidates, key=operator.itemgetter(1), reverse=True)
    return filtered_candidates[0:10]


def classify_sentences(sentences):
    model = load_model('data/bow_model.pkl', glove_path=None, infersent_path=None)
    df = DataFrame(model.predict_proba(sentences), columns=model.classes_)
    df['max'] = df.idxmax(axis=1)
    return df

def prepare_sentence_DF(sentences, obj_a, obj_b):
    index = 0
    temp_list = []
    for sentence in sentences:
        pos_a = find_pos_in_sentence(obj_a, sentence)
        pos_b = find_pos_in_sentence(obj_b, sentence)
        if pos_a < pos_b:
            temp_list.append([obj_a, obj_b, sentence])
        else:
            temp_list.append([obj_b, obj_a, sentence])
        index += 1
    sentence_df = DataFrame.from_records(temp_list, columns=['object_a', 'object_b', 'sentence'])

    return sentence_df


def get_regEx(sequence):
    return re.compile('\\b{}\\b|\\b{}\\b'.format(re.escape(sequence), re.sub('[^a-zA-Z0-9 ]', ' ', sequence)), re.IGNORECASE)

def find_pos_in_sentence(sequence, sentence):
    regEx = get_regEx(sequence)
    match = regEx.search(sentence)    
    if match == None:
        match = regEx.search(re.sub(' +',' ', re.sub('[^a-zA-Z0-9 ]', ' ', sentence)))
        return match.start() if match != None else -1
    else:
        return match.start()