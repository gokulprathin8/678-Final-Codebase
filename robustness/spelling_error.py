import json
import random


def spelling_mistakes(json_data, threshold=0.3):
  modified_json = json_data.copy()

  def make_mistake(word):
    if len(word) > 1:
      # Randomly swap two adjacent characters in the word
      char_index = random.randint(0, len(word) - 2)
      return word[:char_index] + word[char_index + 1] + word[char_index] + word[char_index + 2:]
    return word

  def apply_mistakes_to_sentence(sentence):
    words = sentence.split()
    new_words = [make_mistake(word) if random.random() < threshold else word for word in words]
    return ' '.join(new_words)

  modified_sentences = []
  for sentence in modified_json['sentences']:
    modified_sentence = [apply_mistakes_to_sentence(word) for word in sentence]
    modified_sentences.append(modified_sentence)

  modified_json['sentences'] = modified_sentences

  return modified_json


if __name__ == "__main__":
  with open('../data/test.jsonlines') as f:
    for line in f:
      modified_json = spelling_mistakes(json.loads(line), threshold=0.3)
      with open('../eval-data/spelling_error.jsonlines', 'a') as s:
        s.write(json.dumps(modified_json) + "\n")
