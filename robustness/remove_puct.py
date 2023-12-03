import re
import json

import spacy
import itertools
import spacy_cleaner
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from spacy_cleaner.processing import replacers, removers
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer

nlp = spacy.load("en_core_web_sm")
pipeline = spacy_cleaner.Cleaner(
  nlp,
  removers.remove_punctuation_token,
)
def remove_punctuation(sent):
  return pipeline.clean(sent)


def regex_fuzzy_search(main_string, query_string):
  escaped_query = re.escape(query_string)
  fuzzy_pattern = '.?'.join(escaped_query)
  match = re.search(fuzzy_pattern, main_string)

  if match:
    return match.start(), match.end()
  else:
    return -1, -1

def regex_fuzzy_search_token_list(token_list, query_string):
  escaped_query = re.escape(query_string)
  fuzzy_pattern = '.?'.join(escaped_query)
  for start_index in range(len(token_list)):
    for end_index in range(start_index, len(token_list)):
      token_str = ' '.join(token_list[start_index:end_index + 1])
      if re.search(fuzzy_pattern, token_str):
        return start_index, end_index
  return -1, -1

def fuzzy_search(main_string, query_string):
  if len(query_string) <= 3:
    scorer = fuzz.partial_ratio
    threshold = 80
  else:
    scorer = fuzz.token_set_ratio
    threshold = 70
  matches = process.extract(query_string, [main_string], scorer=scorer)
  potential_matches = [match for match in matches if match[1] >= threshold]

  if potential_matches:
    best_match, score = max(potential_matches, key=lambda x: x[1])
    print(f"Best match: '{best_match}', Score: {score}")
    start_index = main_string.find(best_match)
    if start_index != -1:
      end_index = start_index + len(best_match)
      return start_index, end_index
    else:
      return -1, -1
  else:
    return -1, -1

with open('../data/train.jsonlines') as f:
  for line in f:
    json_line = json.loads(line)
    sentences = json_line['sentences']
    merged_sentence = list(itertools.chain.from_iterable(sentences))
    sentence = TreebankWordDetokenizer().detokenize(merged_sentence)
    for z in json_line['gold_evt_links']:
      event_str = str()
      argument_str = str()

      event_start = z[0][0]
      event_end = z[0][1]
      argument_start = z[1][0]
      argument_end = z[1][1]

      if event_start == event_end:
        event_str = merged_sentence[event_start]
      else:
        event_str = merged_sentence[event_start:event_end]
      if argument_start ==  argument_end:
        argument_str = merged_sentence[argument_start]
      else:
        argument_str = merged_sentence[argument_start:argument_end]

      z[0].append(event_str)
      z[1].append(argument_str)

    punct_removed = remove_punctuation([sentence])
    # print(punct_removed, '\n', sentence)

    for z in json_line['gold_evt_links']:
      event_str = z[0][2]
      argument_str = z[1][2]
      if type(event_str) == list:
        event_str = ' '.join(event_str)
      if type(argument_str) == list:
        argument_str = ' '.join(argument_str)

      tokenized_punct = TreebankWordTokenizer().tokenize(punct_removed[0])
      print(tokenized_punct)

      # event fuzzy search
      new_evt_start, new_evt_end = regex_fuzzy_search_token_list(token_list=tokenized_punct, query_string=event_str)
      # argument fuzzy search
      new_arg_start, new_arg_end = regex_fuzzy_search_token_list(token_list=tokenized_punct, query_string=argument_str)

      print(new_evt_start, new_evt_end, event_str)

      exit(0)







