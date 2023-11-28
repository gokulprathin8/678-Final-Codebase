import nltk
from nltk.corpus import wordnet

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


def replace_nouns_verbs(sentence):
  words = nltk.word_tokenize(sentence)
  pos_tags = nltk.pos_tag(words)

  def get_synonyms(word, tag):
    # Check if the tag is noun (NN) or verb (VB)
    wn_tag = wordnet.NOUN if tag.startswith('NN') else wordnet.VERB if tag.startswith('VB') else None
    if wn_tag is None:
      return []
    return [syn.name().split('.')[0] for syn in wordnet.synsets(word, wn_tag)]

  changed_sentence = ""
  for word, tag in pos_tags:
    synonyms = get_synonyms(word, tag)
    # Replace with the first synonym if available
    changed_word = synonyms[0] if synonyms else word
    changed_sentence += changed_word + " "
  return changed_sentence.strip()


if __name__ == "__main__":
  print(replace_nouns_verbs("Kids love playing in the park on sunny days."))
