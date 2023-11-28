import random


def swap_words(sentence: str, threshold=0.6):
  words = sentence.split()
  if len(words) < 2:
    return sentence
  if random.random() < threshold:
    word1, word2 = random.sample(words, 2)
    index1, index2 = words.index(word1), words.index(word2)
    words[index1], words[index2] = words[index2], words[index1]
  return ' '.join(words)


if __name__ == "__main__":
  swapped_sentence = swap_words("The quick brown fox jumps over the lazy dog.", threshold=0.6)
  print(swapped_sentence)
