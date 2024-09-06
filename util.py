#!/usr/bin/env python

"""Utility strings for use during deployment.

NB: This is not part of the core python code.
"""

import os
import re
import shutil
import time
import click
from fastcore.net import HTTPError
from ghapi.all import GhApi


@click.group()
def cli():
    """Launch the utility CLI."""


@cli.command()
@click.option("--path", default=".test-reports")
def clean_tests(path):
    """Clear up the tests directory.

    NB: Using scripts allows platform independence.
    Creates a new one afterward.
    """
    try:
        shutil.rmtree(path)
        click.echo(f"Removed {path!r}...")
    except OSError:
        click.echo(f"Directory {path!r} does not exist. Skipping...")

    os.mkdir(path)
    click.echo(f"Created {path!r}")


def fetch_latest_draft_release(api):
    """Fetch the latest draft release from the GitHub API."""
    try:
        releases = api.repos.list_releases(per_page=100)
    except HTTPError as err:
        raise click.UsageError(
            "HTTP Error from GitHub API. Check your credentials.\n"
            "(i.e. GITHUB_REPOSITORY_OWNER & GITHUB_TOKEN)\n"
            f"{err}"
        )
    for rel in releases:
        if rel["draft"]:
            return rel
    raise click.UsageError(
        "No draft release found. Ensure your API token has read and write access."
    )


def linkify_prs_and_authors(draft_body):
    """Linkify the PRs and authors in the release body."""
    draft_body_parts = draft_body.split("\n")
    potential_new_contributors = []

    for i, p in enumerate(draft_body_parts):
        draft_body_parts[i] = re.sub(
            r"\(#([0-9]*)\) @([^ ]*)$",
            r"[#\1](https://github.com/python/python/pull/\1) [@\2]"
            r"(https://github.com/\2)",
            p,
        )
        new_contrib_string = re.sub(
            r".*\(#([0-9]*)\) @([^ ]*)$",
            r"* [@\2](https://github.com/\2) made their first contribution in "
            r"[#\1](https://github.com/python/python/pull/\1)",
            p,
        )
        if new_contrib_string.startswith("* "):
            new_contrib_name = re.sub(r"\* \[(.*?)\].*", r"\1", new_contrib_string)
            potential_new_contributors.append(
                {"name": new_contrib_name, "line": new_contrib_string}
            )
    return draft_body_parts, potential_new_contributors


def update_file_with_new_version(filename, new_version_num, keys):
    """Update version number in a given file."""
    with open(filename, "r", encoding="utf8") as input_file:
        lines = input_file.readlines()

    with open(filename, "w", encoding="utf8", newline="\n") as write_file:
        for line in lines:
            for key in keys:
                if line.startswith(key):
                    line = f'{key} = "{new_version_num}"\n'
            write_file.write(line)


@cli.command()
@click.argument("new_version_num")
def release(new_version_num):
    """Change version number in the configuration files."""
    api = GhApi(
        owner=os.environ["GITHUB_REPOSITORY_OWNER"],
        repo="python",
        token=os.environ["GITHUB_TOKEN"],
    )

    latest_draft_release = fetch_latest_draft_release(api)
    is_pre_release = any(char.isalpha() for char in new_version_num)
    click.echo(
        f"Preparing for release {new_version_num}. (Pre-release: {is_pre_release})"
    )

    draft_body_parts, potential_new_contributors = linkify_prs_and_authors(
        latest_draft_release["body"]
    )

    # Handle contributors deduplication
    potential_new_contributors.reverse()
    seen_contributors = set()
    deduped_new_contributors = [
        c for c in potential_new_contributors
        if c["name"] not in seen_contributors and not seen_contributors.add(c["name"])
    ]

    # Update CHANGELOG.md
    click.echo("Updating CHANGELOG.md...")
    with open("CHANGELOG.md", encoding="utf8") as input_changelog:
        input_changelog_lines = input_changelog.readlines()

    with open("CHANGELOG.md", "w", encoding="utf8") as write_changelog:
        write_changelog.writelines(input_changelog_lines)
        # Add the new release details
        write_changelog.write(f"## [{new_version_num}] - {time.strftime('%Y-%m-%d')}\n")
        write_changelog.write("\n".join(draft_body_parts))
        write_changelog.write("\n## New Contributors\n")
        for c in deduped_new_contributors:
            write_changelog.write(f"{c['line']}\n")

    # Update config files
    click.echo("Updating setup.cfg, pyproject.toml, and others...")
    update_file_with_new_version(
        "plugins/python-templater-dbt/setup.cfg",
        new_version_num,
        ["version"]
    )
    update_file_with_new_version(
        "pyproject.toml",
        new_version_num,
        ["version"]
    )

    # Handle non-pre-releases
    if not is_pre_release:
        update_file_with_new_version(
            "pyproject.toml",
            new_version_num,
            ["stable_version"]
        )
        click.echo("Updating gettingstarted.rst...")
        update_file_with_new_version(
            "docs/source/gettingstarted.rst",
            new_version_num,
            ["    $ python version"]
        )

    click.echo("DONE")


if __name__ == "__main__":
    cli()
