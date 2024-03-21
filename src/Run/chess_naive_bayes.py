import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
def read_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data
def generate_san_string_order():
    arquivo = open('san_strings_with_symbols.txt', 'r')
    order = {}
    i = 1
    for linha in arquivo:
        order[linha.strip()] = i
        i = i+1
    return order

data = read_csv('games.csv')
order = generate_san_string_order()
X = []
y = []

for row in data:
    move_sequence = list(map(order.get, row['moves'].split()))
    for move in range(len(move_sequence)):
        if move_sequence[move] == None: move_sequence[move] = 0
    outcome = 1 if row['winner'] == 'black' else 0
    X.append(move_sequence)
    y.append(outcome)
ans = -1
for x in X:
  ans = max(ans, len(x))

for i in range(len(X)):
  for j in range(ans - len(X[i])):
    X[i].append(0)

X = np.array(X)
y = np.array(y)

clf = MultinomialNB()
clf.fit(X, y)

example = "" # nesse exemplo, chance de vencer um jogo (0 movimentos iniciais)
example = example.split()
example = list(map(order.get, example))
for move in range(len(example)):
        if example[move] == None: example[move] = 0
for j in range(ans - len(example)):
    example.append(0)
example = np.array(example)
print("Exemplo dado: tabuleiro vazio")
print("Chance das brancas ganharem:", clf.predict_proba([example])[0][0])
print("Chance das pretas ganharem:", clf.predict_proba([example])[0][1])
print("Acuracia do modelo sobre os dados de treinamento:",accuracy_score(clf.predict(X),y))
