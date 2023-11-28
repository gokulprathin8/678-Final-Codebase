import nltk
import random
from nltk.corpus import wordnet
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')


def get_synonyms(word, pos=None):
  synsets = wordnet.synsets(word, pos=pos)
  synonyms = set()
  for syn in synsets:
    for lemma in syn.lemmas():
      synonyms.add(lemma.name())
  return list(synonyms)


def get_wordnet_pos(tree_tag):
  if tree_tag.startswith('J'):
    return wordnet.ADJ
  elif tree_tag.startswith('V'):
    return wordnet.VERB
  elif tree_tag.startswith('N'):
    return wordnet.NOUN
  elif tree_tag.startswith('R'):
    return wordnet.ADV
  else:
    return None


def replace_with_synonyms(sentence, change_threshold=0.3):
  """Replace words in the sentence with their synonyms based on the threshold."""
  words = word_tokenize(sentence)
  pos_tags = pos_tag(words)

  num_to_replace = int(len(words) * change_threshold)
  replaced_indices = random.sample(range(len(words)), num_to_replace)

  new_words = []
  for i, (word, pos) in enumerate(pos_tags):
    if i in replaced_indices:
      wordnet_pos = get_wordnet_pos(pos)
      synonym_list = get_synonyms(word, pos=wordnet_pos)

      if synonym_list:
        new_word = synonym_list[0].replace('_', ' ')
        new_words.append(new_word)
        continue

    new_words.append(word)

  return ' '.join(new_words)
