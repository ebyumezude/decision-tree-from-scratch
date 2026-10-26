# Decision Tree algorithm — report

Name: Ebelechukwu Umezude

GitHub repository: https://github.com/ebyumezude/decision-tree-from-scratch

PyPI package: **NOT PUBLISHED YET — replace with the actual public PyPI URL after publishing**

## Objective

Implement a decision tree classifier from scratch using entropy and information
gain, with a hyperparameter controlling tree size and a way to display the tree.

## Implementation

The package implements categorical ID3 using Python's standard library.
Entropy measures class impurity. For each candidate feature, information gain
subtracts the weighted entropy of its branches from the current node's entropy.
The feature with maximum gain becomes the split. The procedure repeats within
each branch until a stopping rule applies.

`max_depth` limits depth; the root is at depth zero. `min_samples_split` and
`min_gain` provide additional stopping rules. Leaves predict the majority class.
Unseen categories fall back to the majority class at the current node.
The row identifier Day is excluded. Categories are used directly without encoding.

## Example and results

The lecture's 14-row tennis dataset has nine Yes labels and five No labels.
Its entropy is approximately 0.940286. Root gains are Outlook 0.246750,
Humidity 0.151836, Wind 0.048127 and Temperature 0.029223.
The learned root is Outlook. Sunny splits by Humidity; Rain splits by Wind;
Overcast predicts Yes directly. At max_depth=2 the tree fits all 14 training
examples. At max_depth=0 it predicts the overall majority class, Yes.
Training accuracy is not an estimate of performance on unseen data.

## Display bonus

`display()` prints the learned rules. `export_svg()` generates a graphical
SVG tree that can be opened in a browser or displayed in a notebook.

## Packaging bonus status

The project includes pyproject.toml, package source, README, a license and tests.
It is prepared for publishing, but being packaged locally or uploaded to GitHub
is not the same as being published on PyPI. Update this section after the
public release and include the real package URL and install command.

## Verification and limitations

Tests cover known entropy/gain values, the learned tennis structure, depth
limits, unseen categories, stopping rules, invalid input, and SVG output.
The implementation supports categorical data, not continuous threshold splits.
Missing values must be cleaned first. The dataset is small and no independent
test accuracy is claimed.

## Assistance

Code and explanatory material were prepared with ChatGPT assistance. I should
review, run and understand the implementation before submitting this report.
