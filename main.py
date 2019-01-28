import query_sentences
import extract_candidates
import filter_candidates_wordnet
import filter_candidates_classifier
import filter_candidates_DT
import query_DT_candidates
import object_lists
import visualize_output
import csv
import sys
import calculate_levenshtein_distance
import query_ggl_suggestions
import numpy as np
import os

#CANDIDATES_CSV_PATH = './results/candidates.csv'
CANDIDATES_CSV_PATH = os.path.abspath("/home/hauke/Git/comparison-candidate-retrieval/results/candidates.csv")
#EVALUATION_CSV_PATH = './results/evaluation.csv'
EVALUATION_CSV_PATH = os.path.abspath("/home/hauke/Git/comparison-candidate-retrieval/results/evaluation.csv")
#KEYWORD_TOOL_EXPORTS_DIRECTORY_PATH = '../../Documents/keyword-tool-export/'
KEYWORD_TOOL_EXPORTS_DIRECTORY_PATH = os.path.abspath("/home/hauke/Documents/KeywordToolExport/")

def get_percent_contained(comparison_object, selected_candidates):
    evaluation_candidates = object_lists.evaluation_lists[comparison_object]
    intersection = list(
        set(evaluation_candidates).intersection(selected_candidates))

    return len(intersection) / len(evaluation_candidates)

comparison_objects = []

data = {}
intersections_dict = {}
precisions_dict = {}
recalls_dict = {}
f1_dict = {}

if __name__ == "__main__":
    
    #for comparison_object in object_lists.objects:
    for filename in os.listdir(KEYWORD_TOOL_EXPORTS_DIRECTORY_PATH):
        if filename.endswith(".csv"):
            
            # the comparison object is taken from the keyword tool export file
            comparison_object = filename[22:-7]
            # populate comparison_objects list
            comparison_objects.append(comparison_object)

            # sentences is a list with sentenses that contain the comparison_object AND vs
            sentences = query_sentences.retrieve_sentences(comparison_object)
            # candidates are sentences that match the pattern 'comparison_object vs <nounphrase>' or the other way around
            candidates = extract_candidates.extract_candidates(comparison_object, sentences)

            wordnet_filtered_candidates = filter_candidates_wordnet.filter(comparison_object, candidates)
            
            # append comparison object and 'vs' to suggestions to get the same format as suggestions from the keyword tool
            ccr_suggestions_all = []
            for candidate in wordnet_filtered_candidates:
                ccr_suggestions_all.append(comparison_object + ' vs ' + candidate)
            # top ten results from ccr
            ccr_suggestions_top_ten = ccr_suggestions_all[0:10]
            
            
            # the suggestions as a list of lists
            ggl_api_suggestions = query_ggl_suggestions.get_detailed_suggestions(comparison_object + ' vs')
            # each suggestions stripped of the comparison object and the 'vs'
            ggl_api_suggestions_stripped = [s[len(comparison_object + ' vs '): ] for s in ggl_api_suggestions]

        #first_ten_candidates = candidates#[c[0] for c in candidates]
        #wordnet_filtered_candidates = [] #filter_candidates_wordnet.filter(comparison_object, candicates)
        #classifier_filtered_candidates = [] #filter_candidates_classifier.filter(comparison_object, candicates)
        #DT_filtered_candidates = [] #filter_candidates_DT.filter(comparison_object, candicates)

            # create the intersection set from the keyword-tool-results and worldnet_suggestions
            f = open(KEYWORD_TOOL_EXPORTS_DIRECTORY_PATH + '/' + filename, 'r')
            reader = csv.reader(f, delimiter=',')
            keyword_tool_suggestions = []
            for row in reader:
                for column in row:
                    keyword_tool_suggestions.append(column)

            # the suggestions from the keyword tool are taken as the comparative list
            #comparative_list = keyword_tool_suggestions
            # the suggestions from the keyword tool are taken as the comparative list
            comparative_list = ggl_api_suggestions

            # ~true positives (intersection):
            intersection_set_all = list(set(comparative_list) & set(ccr_suggestions_all))
            true_positives = len(intersection_set_all)
            #intersections_counter.append(true_positives)
            intersections_dict[comparison_object] = true_positives

            intersection_set_stripped = []
            for f in intersection_set_all:
                intersection_set_stripped.append(f[len(comparison_object) + len(' vs '):])

            # ~false negatives:
            false_negatives = len(comparative_list) - true_positives

            # ~false positives:
            false_positives = len(ccr_suggestions_all) - true_positives

            # ~precision:
            if len(ccr_suggestions_all) == 0:
                precision = 0
            else:
                precision = true_positives / len(ccr_suggestions_all)
            #precisions.append(precision)
            precisions_dict[comparison_object] = precision

            # ~recall:
            if len(comparative_list) == 0:
                recall = 0
            else:
                recall = true_positives / len(comparative_list)
            #recalls.append(recall)
            recalls_dict[comparison_object] = recall

            # ~f1score:
            if precision == 0 or recall == 0:
                f1score = 0
            else:
                f1score = 1 / ((1 / recall) + (1 / precision)) / 2
            #f1scores.append(f1score)
            f1_dict[comparison_object] = f1score


            print('--- intersection of ccr suggestions and  all suggestions from the keyword tool: ---')
            print(intersection_set_all)

            with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
                writer = csv.writer(f)
                writer.writerows([['Intersection of ccr suggestions and the suggestions from the keyword tool:']])
                writer.writerow([comparison_object] + intersection_set_all)
                writer.writerows([[ 'keyword tool',                     'ccr',                          'TP',               'FP',               'FN',               'precision',    'recall',   'f1score']])
                writer.writerow(    [len(comparative_list)] +   [len(ccr_suggestions_all)] +    [true_positives] +  [false_positives] + [false_negatives] + [precision] +   [recall] +  [f1score])
                writer.writerows([['keyword tool suggestions:']] + [comparative_list])
                writer.writerows([['ccr suggestions:']] + [ccr_suggestions_all])
                writer.writerows([['intersection']] + [intersection_set_all])
                writer.writerows([['intersection stripped:']] + [intersection_set_stripped])
                writer.writerows([['-----']])

            # len(comparative_list), len(ccr_suggestions_all), true_positives, false_positives, false_negatives, precision ,recall ,f1score
            numericals = [len(comparative_list), len(ccr_suggestions_all), true_positives, false_positives, false_negatives, precision ,recall ,f1score]
            data[comparison_object] = numericals

            continue
        else:
            continue
    
    visualize_output.draw_scatter(comparison_objects, intersections_dict, precisions_dict, recalls_dict, f1_dict)
