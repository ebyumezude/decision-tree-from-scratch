# Finish and publish

## 1. Check locally

Extract the zip, open a terminal inside decision-tree-homework, and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python examples/tennis_demo.py
python -m unittest discover -s tests -v
```

Open tree.svg in a browser. Keep .venv out of GitHub.

## 2. GitHub

Create a repository in your GitHub account, for example `decision-tree-from-scratch`.
Use GitHub's Add file > Upload files to upload the CONTENTS of the extracted
folder, preserving src/, examples/ and tests/. Do not upload just the zip.
If using a terminal instead, follow GitHub's displayed commands for your new
repository. Do not upload .venv/, build/, dist/, API tokens or account secrets.

Replace the GitHub placeholder in report.md with your actual repository URL.
Keep the large irrigation CSVs out of this homework repository.
The separate Kaggle repository should contain the completed irrigation notebook,
a README describing its dataset/metric/results and environment requirements.
Use a data-source link instead of copying competition data without permission.

## 3. Prepare PyPI

PyPI (Python Package Index) is https://pypi.org, not the alternative interpreter PyPy.
Create/verify your account and complete the security setup required by PyPI.
Check whether the distribution name `ebele-entropy-tree` is available.
If taken, edit only project.name in pyproject.toml to a unique name; the import
name remains ebele_tree. Do this before building.

## 4. Build and check

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

This should produce a wheel (.whl) and source archive (.tar.gz).
If you change the package name/version, remove old files from dist/ before
rebuilding, so you do not accidentally upload a previous build.

## 5. Publish to the real PyPI for the bonus

After you have reviewed the package and are ready to make it public:

```bash
python -m twine upload dist/*
```

Use a PyPI API token via the secure prompt (username __token__ if requested).
Never place tokens in code, report.md, GitHub, screenshots or this chat.
TestPyPI is a separate service and does not by itself satisfy a real PyPI release.

When upload succeeds, open the package's actual PyPI page. In a fresh environment,
install it using the exact distribution name you published:

```bash
python -m pip install ebele-entropy-tree==0.1.0
python -c "from ebele_tree import entropy; print(entropy(['Yes', 'No']))"
```

If you chose a different name, replace ebele-entropy-tree in the install command.
Expected output is 1.0. Add the actual PyPI URL and install command to report.md,
update the bonus status to describe what actually succeeded, then update GitHub.
Published versions cannot be overwritten: use a higher version for later fixes.

## 6. Submit the assignment

Check report.md has real links and no unfinished placeholders. Read it and edit
the description to match your understanding and actual actions. Attach report.md
to the Teams assignment and click Turn in before the displayed 23:59 deadline.

Official packaging guide:
https://packaging.python.org/en/latest/tutorials/packaging-projects/
