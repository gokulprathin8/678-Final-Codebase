import itertools
from pprint import pprint
import json
import random
from typing import List

import numpy as np
import spacy
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer, TreebankWordTokenizer

def swap_words(sentence: str, threshold=0.6, words_to_exclude=None):
  words = sentence.split()
  if words_to_exclude is None:
    words_to_exclude = []
  words_to_swap = [word for word in words if word not in words_to_exclude]

  if len(words_to_swap) < 2 or random.random() >= threshold:
    return sentence

  word1, word2 = random.sample(words_to_swap, 2)
  index1, index2 = words.index(word1), words.index(word2)
  words[index1], words[index2] = words[index2], words[index1]

  return ' '.join(words)

def flatten(lst):
  flat_list = []
  for item in lst:
    if isinstance(item, list):
      flat_list.extend(flatten(item))
    else:
      flat_list.append(item)
  return flat_list


if __name__ == "__main__":
  with open('../data/train.jsonlines') as f:
    for line in f:
      dict_mapping = dict()
      before_swap_vals = list()
      json_line = json.loads(line)
      sentences = json_line['sentences']
      merged_sentences = list(itertools.chain.from_iterable(sentences))

      # split sentence into editable and non-editable sub-strings
      sentence = TreebankWordDetokenizer().detokenize(merged_sentences)
      static_strings = list()
      for z in json_line['gold_evt_links']:
        event_str = str()
        argument_str = str()

        event_start = z[0][0]
        event_end = z[0][1]
        argument_start = z[1][0]
        argument_end = z[1][1]
        event_name = z[2]

        if event_start == event_end:
          event_str = merged_sentences[event_start]
        else:
          event_str = merged_sentences[event_start:event_end]
        if argument_start == argument_end:
          argument_str = merged_sentences[argument_start]
        else:
          argument_str = merged_sentences[argument_start:argument_end]

        static_strings.append(event_str)
        static_strings.append(argument_str)
      excluded_words = flatten(static_strings)
      swapped_sentence = swap_words(sentence, words_to_exclude=excluded_words)

      tokenized_sentence  = TreebankWordTokenizer().tokenize(swapped_sentence)
      arr_sizes: List[int] = list()
      for z in sentences:
        arr_sizes.append(len(z))  # getting existing shape
      new_sents = list()
      for z in arr_sizes:
        new_sents.append(tokenized_sentence[:z])
        del tokenized_sentence[:z]
      json_line['sentences'] = new_sents
      with open('../eval-data/swapping_words.jsonlines', 'a') as s:
        s.write(json.dumps(json_line) + "\n")





