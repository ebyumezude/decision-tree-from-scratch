import csv
from pathlib import Path
from ebele_tree import DecisionTreeClassifier, entropy, information_gain

with Path(__file__).with_name("tennis.csv").open() as f:
    rows = list(csv.DictReader(f))
y = [row["Play_Tennis"] for row in rows]
X = [{k: v for k, v in row.items() if k not in ("Day", "Play_Tennis")} for row in rows]
print("Dataset entropy:", round(entropy(y), 6))
for feature in X[0]:
    print(feature, "gain:", round(information_gain([r[feature] for r in X], y), 6))
model = DecisionTreeClassifier(max_depth=2).fit(X, y)
model.display()
print("Training accuracy (not unseen-data accuracy):", model.score(X, y))
print("New Sunny/High day:", model.predict([X[0]]))
model.export_svg("tree.svg")
print("Open tree.svg in your browser to see the tree.")
