---
title: Testing
hide: navigation
---
<!--
SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
SPDX-License-Identifier: CC-BY-4.0
-->

<!-- markdownlint-disable-next-line MD025 -->
# Testing

This projects provides a few different tests and checks.

In general, we have two files which define all the tests:

- [.pre-commit-config.yaml](https://github.com/DLR-KI/md-multiline-table/blob/main/.pre-commit-config.yaml)
- [.github/workflows/main.yml](https://github.com/DLR-KI/md-multiline-table/blob/main/.github/workflows/main.yml)
<!--
- [.gitlab-ci.yml](https://github.com/DLR-KI/md-multiline-table/blob/main/.gitlab-ci.yml)
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

## Python Code Tests

Feature tests as well as test coverage:

```bash
# run tests
python -m coverage run -m unittest discover --start-directory tests

# create html coverage report
python -m coverage html --directory "./build/htmlcov"
# serve html coverage report
python -m http.server -d build/htmlcov
```

Static code checks using [ruff](https://docs.astral.sh/ruff):

```bash
# linter
python -m ruff check md_multiline_table
python -m ruff check tests
# formatter
python -m ruff format --diff md_multiline_table
python -m ruff format --diff tests
```

To run automatic static code fixes, use:

```bash
# linter
python -m ruff check --fix md_multiline_table
python -m ruff check --fix tests
# formatter
python -m ruff format md_multiline_table
python -m ruff format tests
```

Static type checks using [mypy](https://www.mypy-lang.org/):

```bash
python -m mypy md_multiline_table
python -m mypy tests
```

## Markdown Checks

Verify documentation (markdown) compliance w.r.t. [markdown linting rules](https://github.com/DavidAnson/markdownlint#rules--aliases) further specified inside the [.markdownlint-cli2.jsonc](https://github.com/DLR-KI/md-multiline-table/blob/main/.markdownlint-cli2.jsonc) configuration file.

```bash
npm exec markdownlint-cli2 -- "./docs/**/*.md" "./README.md"
```

## License Checks

```bash
python -m licensecheck
python -m reuse lint
```

## Vulnerability Checks

```bash
python -m tox --recreate -e vulnerability
```
