import json

from nltk.tokenize.treebank import TreebankWordDetokenizer

import cvt_active_passive


def get_context(*, json_data, merged_sentence):
  events = json_data['gold_evt_links']
  event_frame = dict()
  for e in events:
    event_end = e[0]
    event_start = e[1]
    event_type = e[2]

    if event_start >= event_end:
      tmp = event_start
      event_start = event_end
      event_end = tmp
    event_frame[event_type] = TreebankWordDetokenizer().detokenize(merged_sentence[event_start[1]:event_end[1]])
  return event_frame


def process_train_data():
  data = list()
  with open('data/train.jsonlines', mode='r') as f:
    for line in f:
      current_line = json.loads(line)
      data.append(current_line)
      # source = current_line['source_url']
      sentences = current_line['sentences']
      merged_sentence = [item for sublist in sentences for item in sublist]
      complete_sentence = TreebankWordDetokenizer().detokenize(merged_sentence)
      context = get_context(json_data=current_line, merged_sentence=merged_sentence)
      print(complete_sentence, context)

      print('\n ---------')
      for c in context.values():
        # check if context is active or passive
        is_passive_sent = cvt_active_passive.is_passive(c)
        if is_passive_sent:
          # if sentence is passive, convert it to active
          converted_sent = cvt_active_passive.convert_passive_to_active(c)
        else:
          # if sentence is active, convert it to passive
          converted_sent = cvt_active_passive.convert_active_to_passive(c)
        print(f'\n\nExisting: {c}\n Converted: {converted_sent}')
      exit(0)


process_train_data()
