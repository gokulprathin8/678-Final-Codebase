import random


def spelling_mistakes(sentence, threshold=0.3):
  def make_mistake(word):
    if len(word) > 1:
      # Randomly swap two adjacent characters in the word
      char_index = random.randint(0, len(word) - 2)
      return word[:char_index] + word[char_index + 1] + word[char_index] + word[char_index + 2:]
    return word

  words = sentence.split()
  new_words = [make_mistake(word) if random.random() < threshold else word for word in words]
  return ' '.join(new_words)


if __name__ == "__main__":
  print(spelling_mistakes("the quick brown fox jumps over the lazy dog"))

