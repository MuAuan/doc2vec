import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

words = defaultdict(lambda: 0)
for line in open(args.input, "r", encoding="utf-8", errors='ignore'):
    line = line.strip()
    if line == "" or line[0] == "<":
        continue
    for word in line.split(" "):
        words[word] += 1
print("word num : ", len(words))

few_word_num = 0
with open(args.output, "w", encoding="utf-8") as f:
    for word in words:
        if words[word] <= 2: #10
            few_word_num += 1
            f.write(word)
            f.write("\n")
print("few word num : ", few_word_num)
                    