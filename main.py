import query_sentences



if __name__ == "__main__":
    comparison_object = 'python'
    sentences = query_sentences.retrieve_sentences(comparison_object)
    print(sentences)