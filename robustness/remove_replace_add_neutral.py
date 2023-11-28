import random

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')


def auto_word_modification(sentence: str, threshold=0.2):
  stop_words = set(stopwords.words('english'))
  neutral_words = ["something", "thing", "area", "case", "day"]  # Example list of neutral words
  words = sentence.split()
  modified = []
  for word in words:
    if random.random() < threshold:
      if word.lower() not in stop_words:
        modified.append(random.choice(neutral_words) if random.random() < 0.5 else word)
    else:
      if word.lower() not in stop_words:
        modified.append(word)
  if random.random() < threshold:
    modified.append(random.choice(neutral_words))
  return ' '.join(modified)


if __name__ == '__main__':
  sentence = "This is a sample sentence with a few common words"
  modified_sentence = auto_word_modification(sentence, threshold=0.2)
  print(modified_sentence)
