<!--
SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
SPDX-License-Identifier: CC-BY-4.0
-->

# Multiline Table extension for Python Markdown

This project extends the Python markdown implementation with multiline table support.

![md multiline table](/docs/images/md-multiline-table.png)

A good starting point is the documentation published on the [GitHub Pages](https://dlr-ki.github.io/md-multiline-table).
The following information and instructions in this README are mostly aimed at developers and contributors.

## Repository Structure

The repository is organized as follows:

- [docs](docs): Markdown-based user documentation published on the [GitHub Pages](https://dlr-ki.github.io/md-multiline-table).
- [LICENSES](LICENSES): All license files used somewhere in this project. Also see [LICENSE.md](LICENSE.md).
- [md_multiline_table](md_multiline_table): Project source code.
- [tests](tests): Project tests.

## Requirements

- Python 3.7 or later as well as pip

    ```bash
    which python
    python --version
    which pip
    ```

- virtualenv or venv (highly recommended)

    ```bash
    pip install -U virtualenv
    ```

## Install

There are multiple optional dependencies available:

- `dev`: installs additional development tools
- `test`: installs test requirements
- `stubs`: installs further type information
- `docs`: installs documentation requirements
- `all`: installs all optional dependencies

Of course, it is possible to install the software without any additional optional dependencies.
Choose your poision based on your own requirements.

```bash
# create virtual environment
virtualenv -p $(which python3.10) .venv
# or
# python -m venv .venv

# activate our virtual environment
source .venv/bin/activate

# update pip (optional)
python -m pip install -U pip

# install
pip install -U -e ".[all]"

# enable git pre-commit hooks (optional)
pre-commit install
```

## Usage

### markdown package

```python
from markdown import markdown
from md_multiline_table import MultilineTableExtension

html = markdown(text, extensions=[MultilineTableExtension()])
```

### mkdocs

Just add `md-multiline-table` inside the `markdown_extensions` of your `mkdocs.yml` file.

```yaml
markdown_extensions:
  - md-multiline-table
```

## Testing

This projects provides a few different tests and checks.

> [!Note]
> For detailed information about the tests, please check out the
> [Testing](https://dlr-ki.github.io/md-multiline-table/testing) section in the documentation.

In general, we have two files which defines all the tests:

- [.pre-commit-config.yaml](.pre-commit-config.yaml)
- [.github/workflows/main.yml](.github/workflows/main.yml)
<!--
- [.gitlab-ci.yml](.gitlab-ci.yml)
-->

To run the pre-commit hooks manually, use:

```bash
pre-commit run --all-files
```

Running the GitLab CI locally is a bit more complicated.
Is also requires Node.js as well as Docker installed and configured.

```bash
npm exec gitlab-ci-local
# or run a single job, e.g. pre-commit
npm exec gitlab-ci-local -- pre-commit
```

## Contribution

Please follow the contribution rules:

- use typed Python (type annotations)
- verify Python static code checks with ruff
- write tests
- document fixes, enhancements, new features, ...
- write scripts and examples OS independent or at least with linux, wsl support
- verify shell script static code check compliance with [ShellCheck](https://www.shellcheck.net/wiki/)
- verify [REUSE Specification 3.0](https://reuse.software/spec/) compliance for all files
- verify project license compliance without any license conflicts (e.g. for 3rd party libraries, data, models, ...)
- verify documentation (markdown) compliance w.r.t. [markdown linting rules](https://github.com/DavidAnson/markdownlint#rules--aliases) further specified inside the [.markdownlint-cli2.jsonc](.markdownlint-cli2.jsonc) configuration file
- run all tests successfully

### Documentation

This projects is using the Docstring style from [Google](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).
At least public classes, methods, fields, ... should be documented.

For further documentation we are using [Markdown](https://www.markdownguide.org/) documentation with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
See the [docs](docs) folder for more details.

To locally serve the documentation, feel free to use:

```bash
python -m mkdocs serve
```

### Contributors

<a href="https://github.com/HeinrichAD">
  <img
    src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/5962361?v=4&h=80&w=80&fit=cover&mask=circle&maxage=7d"
    alt="Florian Heinrich"
    title="Florian Heinrich"
  />
</a>

## Citation

For accurate citation, refer to the corresponding metadata in the [CITATION.cff](CITATION.cff) file associated with this work.
<!-- or reference directly to the deposit on Zenodo [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.ZENODO-DOI.svg)](https://doi.org/10.5281/zenodo.ZENODO-DOI). -->

## License

Please see the file [LICENSE.md](LICENSE.md) for further information about how the content is licensed.
