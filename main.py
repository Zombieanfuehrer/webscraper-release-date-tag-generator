import os
import argparse

from web_scrapper import WebScrapper
from date_formatter import DateFormatter
from git_lab_tag_manager import GitLabTagManager


def main():
    parser = argparse.ArgumentParser(
        description="Extract date from a webpage and create a GitLab tag."
    )
    parser.add_argument(
        "--webpage_url",
        required=True,
        help="URL of the webpage to extract string from",
    )
    parser.add_argument("--project_id", required=True, help="GitLab project ID")
    parser.add_argument("--private_token", required=True, help="GitLab private token")
    parser.add_argument("--regex", required=True, help="Regex pattern to search for")

    args = parser.parse_args()

    url = args.webpage_url
    project_id = args.project_id
    private_token = args.private_token
    pattern = args.regex

    web_scrapper = WebScrapper(url)
    try:
        grabbed = web_scrapper.scrap_string(pattern)
    except Exception as e:
        print(e)
        return

    release_date_edition = grabbed[0]
    formatted_date = DateFormatter.format_date(release_date_edition)


    git_lab_tag_manager = GitLabTagManager(project_id, private_token)
    if git_lab_tag_manager.tag_exists(formatted_date):
        print(f"Tag '{formatted_date}' already exists.")
        return
    else:
        try:
            git_lab_tag_manager.create_tag(formatted_date, "master", "Tagged by web scrapper")
            print(f"Tag '{formatted_date}' has been created.")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
