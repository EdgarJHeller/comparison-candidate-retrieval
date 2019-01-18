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


if __name__ == "__main__":
    # write headlines to candidates csv
    #with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
    #    writer = csv.writer(f)
    #    writer.writerows([['Comparison Object:', 'Candidates:']])

    # write headlines to evaluation csv
    #with open(EVALUATION_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
    #    writer = csv.writer(f)
    #    writer.writerows([['ccr vs google', 'Comparison Object:', 'Levenshtein Distance Minima', 'LDM Sum', 'Matching Suggestions Sum']])

    # the comparison object is now set as third parameter when main is called
    # eg: python main.py reader reader python -> comparison object is "python"
    #comparison_object = sys.argv[3]
    
    #for comparison_object in object_lists.objects:
    for filename in os.listdir(KEYWORD_TOOL_EXPORTS_DIRECTORY_PATH):
        if filename.endswith(".csv"):
            
            # the comparison object is taken from the keyword tool export file
            comparison_object = filename[22:-7]

            # sentences is a list with sentenses that contain the comparison_object AND vs
            sentences = query_sentences.retrieve_sentences(comparison_object)
            candidates = extract_candidates.extract_candidates(comparison_object, sentences)
            # all
            wordnet_filtered_candidates_all = filter_candidates_wordnet.filter(comparison_object, candidates)
            # 1st ten
            wordnet_filtered_candidates_1st_ten = [c[0] for c in wordnet_filtered_candidates_all[0:10]]
            
            
            # the suggestions as a list of lists
            ggl_api_suggestions = query_ggl_suggestions.get_suggestions(comparison_object + ' vs')
            # the suggestions as a list of strings
            ggl_api_suggestions = [item[0] for item in ggl_api_suggestions]
            # each suggestions stripped of the comparison object and the 'vs'
            ggl_api_suggestions_stripped = [s[len(comparison_object + ' vs '): ] for s in ggl_api_suggestions]


            # create the intersection set from the keyword-tool-results and worldnet_suggestions
            f = open(KEYWORD_TOOL_EXPORTS_DIRECTORY_PATH + '/' + filename, 'r')
            reader = csv.reader(f, delimiter=',')
            keyword_tool_suggestions = []
            for row in reader:
                for column in row:
                    keyword_tool_suggestions.append(column)
            worldnet_suggestions_1st_ten = []
            for candidate in wordnet_filtered_candidates_1st_ten:
                worldnet_suggestions_1st_ten.append(comparison_object + ' vs ' + candidate)
            worldnet_suggestions_all = []
            for candidate in wordnet_filtered_candidates_all:
                worldnet_suggestions_all.append(comparison_object + ' vs ' + candidate)
            # all
            intersection_set_all = list(set(keyword_tool_suggestions) & set(worldnet_suggestions_1st_ten))
            # 1st ten
            intersection_set_first_ten = list(set(ggl_api_suggestions) & set(worldnet_suggestions_1st_ten))


            print('--- intersection of ccr suggestions and  all suggestions from the keyword tool: ---')
            print(intersection_set_all)
            print('--- intersection of ccr suggestions and 1st ten keyword tool suggestions: ---')
            print(intersection_set_first_ten)

            with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
                writer = csv.writer(f)
                writer.writerows([['Intersection ccr suggestions with first ten google suggestions from google api:']])
                writer.writerow([comparison_object] + intersection_set_first_ten)
                writer.writerows([['Intersection ccr suggestions with all of google suggestions from keyword tool:']])
                writer.writerow([comparison_object] + intersection_set_all)

            #with open(EVALUATION_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
            #    writer = csv.writer(f)
            #    writer.writerows([['ccr vs google api',     'Comparison Object:',   'Levenshtein Distance Minima',  'LDM Sum', 'Matching Suggestions Sum']])
            #    writer.writerow(['ccr vs google 1st ten'] + [comparison_object] +   [levenshtein_distance_minima] + [lcm_sum] + [matching_suggestions_sum])
            
            continue
        else:
            continue
