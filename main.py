import json
from pprint import pprint
from nltk.tokenize.treebank import TreebankWordDetokenizer

from robustness.synonyms import replace_with_synonyms


def get_context(*, json_data, merged_sentence):
  events = json_data['gold_evt_links']
  event_frame = []

  for e in events:
    event, argument, event_type = e[0], e[1], e[2]
    event_start, event_end = event[0], event[1]
    argument_start, argument_end = argument[0], argument[1]

    # Adjust slicing to extract correct context
    event_ctx = merged_sentence[event_start:event_end + 1]
    argument_ctx = merged_sentence[argument_start:argument_end + 1]

    event_ctx_text = ' '.join(event_ctx)
    argument_ctx_text = ' '.join(argument_ctx)

    event_frame.append({
      'Event': event_ctx_text,
      'Argument': argument_ctx_text,
      'Event_Type': event_type,
      'Event_Position': (event_start, event_end),
      'Argument_Position': (argument_start, argument_end)
    })

  return event_frame



def process_test_data():
  data = list()
  with open('data/test.jsonlines', mode='r') as f:
    for line in f:
      current_line = json.loads(line)
      data.append(current_line)
      sentences = current_line['sentences']
      merged_sentence = [item for sublist in sentences for item in sublist]
      complete_sentence = TreebankWordDetokenizer().detokenize(merged_sentence)
      context = get_context(json_data=current_line, merged_sentence=merged_sentence)
      # pprint(context)

      updated_json = replace_with_synonyms(complete_sentence, context)
      pprint(updated_json)

      exit(0)


process_test_data()
