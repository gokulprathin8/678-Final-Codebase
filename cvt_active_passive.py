import nltk
import spacy
from nltk.corpus import wordnet
from spacy.symbols import *

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

nlp = spacy.load('en_core_web_sm')

pronouns = {'her ':'she ', 'him ':'he ', 'whom ':'who ', 'me ': 'I ', 'us ':'we ', 'them ':'they '}

def is_passive(sentence):
  tokens = nltk.word_tokenize(sentence)
  tagged = nltk.pos_tag(tokens)
  grammar = r"""
        PASSIVE: {<VB.?|MD>+<RB.*>*<VBN>+}
    """
  chunk_parser = nltk.RegexpParser(grammar)
  tree = chunk_parser.parse(tagged)
  for subtree in tree.subtrees():
    if subtree.label() == 'PASSIVE':
      return True

  return False


def get_lemma(word):
  lemmas = wordnet.lemmas(word, pos='v')
  if lemmas:
    return lemmas[0].name()
  return word



def convert_active_to_passive(sentence):
  doc = nlp(sentence)
  subject = str()
  verb = str()
  obj = str()

  for token in doc:
    if token.dep == nsubj:
      subject = token.text
    elif token.pos == VERB:
      verb = token.lemma_
    elif token.dep == dobj:
      obj = token.text

  if not subject or not verb or not obj:
    return "Error converting to passive voice."

  passive_verb = get_lemma(verb) + "ed" if verb != "be" else verb
  passive_sentence = f"{obj} was {passive_verb} by {subject}"
  return passive_sentence


def convert_passive_to_active(sentence):
  global base_form_of_main_verb, main_verb, compound_article, recipient
  doc = nlp(sentence)
  for sent in doc.sents:
    try:
      sent_list = []
      for token in sent:
        sent_list.append(token)

      main_verb_index = None
      agent_index = None
      recipient_index = None
      agent = ''
      append = False
      inflection = ''
      agent_article = ''
      start_word = ''
      sentence_remainder = []

      index_counter = 0

      for token in sent_list:
        if token.dep_ in ['nsubjpass', 'nsubj']:
          recipient_index = index_counter
          recipient = token.lower_
          article_list = [t.text for t in token.lefts]
          try:
            compound_article = ' '.join(article_list).lower()
          except:
            compound_article = ''
        if token.dep_ == 'ROOT':
          main_verb_index == index_counter
          main_verb = token.text
          base_form_of_main_verb = token.lemma_

        if token.dep_ == 'agent':
          agent_index = index_counter
          agent_children_list = [t.text for t in token.rights]
          agent_children_right = ' '.join(agent_children_list)
          agent = token.text + ' ' + agent_children_right
          agent_children_left = [t.text for t in token.lefts]
          append = True
        if agent and not token.is_punct:
          sentence_remainder.append(token)
        if token.is_punct:
          punct = token.text
        if token.dep_ == 'pobj':
          append = False
          if not agent:
            agent = token.text
        if token.text in ['may', 'must', 'might', 'could', 'will']:
          inflection = ' ' + token.text + ' '

        index_counter += 1
      if punct in ['?']:
        for token in sent:
          if token.text in ['Can', 'May']:
            start_word = token.text
            break

      for key, value in pronouns.items():
        if key in agent.lower() + ' ':
          agent = value.strip()
      index = 0
      for t in sentence_remainder:
        if t.pos_ in ['DET'] and index >= 2:
          agent_article = t.text
          index += 1

      if recipient_index < agent_index:
        print('-'*50+'\n {}'.format(
          sent)+'\n Active voice skeleton:{} {} {} {}{} {} {}{}'.format(
          start_word, agent_article, agent, inflection, main_verb, compound_article, recipient, punct).replace(
          'by ', ''))
        print('Base form of main verb: {}'.format(base_form_of_main_verb))
    except Exception as e:
      print(sent)
      for token in sent:
        print('Text: ' + token.text + ' |   Dep: ' + token.dep_ + ' |   Tag: ' + token.tag_)

