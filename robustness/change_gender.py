import json


def change_gender(json_data):
  modified_json = json_data.copy()

  gender_map = {'he': 'she', 'she': 'he', 'his': 'her', 'her': 'his'}

  def change_gender_in_sentence(sentence):
    words = sentence.split()
    new_words = [gender_map.get(word.lower(), word) for word in words]
    return ' '.join(new_words)

  modified_sentences = []
  for sentence in modified_json['sentences']:
    modified_sentence = [change_gender_in_sentence(word) for word in sentence]
    modified_sentences.append(modified_sentence)

  modified_json['sentences'] = modified_sentences

  return modified_json

if __name__ == '__main__':
  with open('../data/test.jsonlines') as f:
    for line in f:
      modified_json = change_gender(json.loads(line))
      with open('../eval-data/change_gender.jsonlines', 'a') as s:
        s.write(json.dumps(modified_json) + "\n")
