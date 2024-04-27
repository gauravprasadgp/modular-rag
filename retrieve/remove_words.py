import spacy
nlp = spacy.load("en_core_web_sm")
sentences_list = ["I like big planes.", "No, I saw no big flames."]
new_sentence_list = []
customize_stop_words = [
    'planes', 'flames'
]

for w in customize_stop_words:
    nlp.vocab[w].is_stop = True

for i in sentences_list:
    doc = nlp(i)
    new_sentence_list.append(" ".join([token.text for token in doc if not token.is_stop and not token.is_punct]))

print(new_sentence_list)