"""Categorical ID3 tree. Uses only Python's standard library."""
from collections import Counter
from html import escape
from math import log2
from pathlib import Path


def entropy(labels):
    """Shannon entropy in bits; an empty or pure group has entropy zero."""
    labels = list(labels)
    counts = Counter(labels)
    return -sum((n / len(labels)) * log2(n / len(labels))
                for n in counts.values()) if labels else 0.0


def information_gain(values, labels):
    """Parent entropy minus weighted child entropies."""
    values, labels = list(values), list(labels)
    if len(values) != len(labels) or not labels:
        raise ValueError("Provide equally sized, nonempty values and labels.")
    groups = {}
    for value, label in zip(values, labels):
        groups.setdefault(value, []).append(label)
    return entropy(labels) - sum(len(group) / len(labels) * entropy(group)
                                 for group in groups.values())


class DecisionTreeClassifier:
    """ID3 for categorical features, supplied as a list of dictionaries.

    max_depth=0 gives a majority-class leaf; None allows unrestricted depth.
    min_samples_split and min_gain provide additional stopping controls.
    Unseen categories fall back to the current node's majority class.
    Numeric values, if supplied, are discrete categories, NOT thresholds.
    Missing values are not supported: clean/impute them before fitting.
    """
    def __init__(self, max_depth=None, min_samples_split=2, min_gain=1e-12):
        if max_depth is not None and (type(max_depth) is not int or max_depth < 0):
            raise ValueError("max_depth must be None or a nonnegative integer.")
        if type(min_samples_split) is not int or min_samples_split < 2:
            raise ValueError("min_samples_split must be an integer >= 2.")
        if not isinstance(min_gain, (int, float)) or not 0 <= min_gain < float('inf'):
            raise ValueError("min_gain must be a finite nonnegative number.")
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_gain = min_gain

    def fit(self, X, y):
        X, y = list(X), list(y)
        if not X or len(X) != len(y):
            raise ValueError("X and y must be nonempty and have equal lengths.")
        if not all(isinstance(row, dict) for row in X):
            raise ValueError("X must contain dictionaries.")
        self.features_ = list(X[0])
        if any(set(row) != set(self.features_) for row in X):
            raise ValueError("All rows must have the same feature names.")
        for value in [v for row in X for v in row.values()] + y:
            if value is None or value != value:
                raise ValueError("Missing values must be cleaned first.")
            hash(value)
        self.tree_ = self._build(X, y, self.features_, 0)
        return self

    def _build(self, X, y, features, depth):
        # Counter preserves appearance order, making majority ties deterministic.
        majority = Counter(y).most_common(1)[0][0]
        node = {"prediction": majority, "samples": len(y), "entropy": entropy(y)}
        if (len(set(y)) == 1 or not features or len(y) < self.min_samples_split
                or (self.max_depth is not None and depth >= self.max_depth)):
            return node
        gains = {f: information_gain([row[f] for row in X], y) for f in features}
        best = max(gains, key=gains.get)
        if gains[best] <= self.min_gain:
            return node
        node.update(feature=best, gain=gains[best], children={})
        remaining = [f for f in features if f != best]
        for value in dict.fromkeys(row[best] for row in X):
            indices = [i for i, row in enumerate(X) if row[best] == value]
            node["children"][value] = self._build(
                [X[i] for i in indices], [y[i] for i in indices], remaining, depth + 1)
        return node

    def _check_fitted(self):
        if not hasattr(self, "tree_"):
            raise ValueError("Call fit before predicting or displaying the tree.")

    def predict(self, X):
        self._check_fitted()
        predictions = []
        for row in X:
            node = self.tree_
            while "feature" in node:
                feature = node["feature"]
                if feature not in row:
                    raise ValueError("Missing prediction feature: " + feature)
                if row[feature] not in node["children"]:
                    break
                node = node["children"][row[feature]]
            predictions.append(node["prediction"])
        return predictions

    def score(self, X, y):
        y = list(y)
        predictions = self.predict(X)
        if not y or len(y) != len(predictions):
            raise ValueError("Provide equally sized, nonempty X and y.")
        return sum(a == b for a, b in zip(predictions, y)) / len(y)

    def display(self):
        """Print the learned rules with indentation showing each branch."""
        self._check_fitted()
        lines = []
        def visit(node, indent=""):
            if "feature" not in node:
                lines.append(f"{indent}Predict {node['prediction']} (n={node['samples']})")
            else:
                lines.append(f"{indent}{node['feature']} (gain={node['gain']:.3f})")
                for value, child in node["children"].items():
                    lines.append(f"{indent}  If {node['feature']} = {value}:")
                    visit(child, indent + "    ")
        visit(self.tree_)
        print("\n".join(lines))

    def export_svg(self, filename="tree.svg"):
        """Save a graphical tree, viewable directly in a web browser."""
        self._check_fitted()
        nodes, edges = [], []
        leaf_count = 0
        def layout(node, depth):
            nonlocal leaf_count
            children = []
            for value, child in node.get("children", {}).items():
                children.append((value, layout(child, depth + 1)))
            if children:
                x = sum(child[0] for _, child in children) / len(children)
            else:
                x = 140 + leaf_count * 240
                leaf_count += 1
            y = 60 + depth * 150
            for value, child in children:
                edges.append((x, y, child[0], child[1], str(value)))
            label = str(node.get("feature", "Predict: " + str(node["prediction"])))
            nodes.append((x, y, label, node['samples']))
            return x, y
        layout(self.tree_, 0)
        width, height = max(280, leaf_count * 240 + 40), max(n[1] for n in nodes) + 60
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
               '<rect width="100%" height="100%" fill="white"/>']
        for x1, y1, x2, y2, label in edges:
            svg.append(f'<line x1="{x1}" y1="{y1+27}" x2="{x2}" y2="{y2-27}" stroke="#53677d"/>')
            svg.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2}" text-anchor="middle" font-family="sans-serif" font-size="14">{escape(label)}</text>')
        for x, y, label, samples in nodes:
            svg.append(f'<rect x="{x-100}" y="{y-27}" width="200" height="54" rx="10" fill="#e4effb" stroke="#376aa0"/>')
            svg.append(f'<text x="{x}" y="{y-3}" text-anchor="middle" font-family="sans-serif" font-size="15">{escape(label)}</text>')
            svg.append(f'<text x="{x}" y="{y+17}" text-anchor="middle" font-family="sans-serif" font-size="12">n={samples}</text>')
        svg.append('</svg>')
        Path(filename).write_text("\n".join(svg), encoding="utf-8")
        return str(filename)
