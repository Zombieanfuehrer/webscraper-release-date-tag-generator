import argparse
from web_scrapper import WebScrapper
from date_formatter import DateFormatter
from git_lab_tag_manager import GitLabTagManager


def main():
    parser = argparse.ArgumentParser(description="Extract date from a webpage and create a GitLab tag.")
    parser.add_argument("--webpage_url", required=True, help="URL of the webpage to extract string from")
    parser.add_argument("--project_id", required=True, help="GitLab project ID")
    parser.add_argument("--private_token", required=True, help="GitLab private token")
    parser.add_argument("--regex", required=True, help="Regex pattern to search for")
    args = parser.parse_args()

    try:
        web_scrapper = WebScrapper(args.webpage_url)
        release_date_edition = web_scrapper.scrap_string(args.regex)
        print(f"Extracted string: {release_date_edition}")

        formatted_date = DateFormatter.format_date(release_date_edition)
        print(f"Formatted date: {formatted_date}")

        git_lab_tag_manager = GitLabTagManager(args.project_id, args.private_token)
        if git_lab_tag_manager.tag_exists(formatted_date):
            print(f"Tag '{formatted_date}' already exists.")
        else:
            git_lab_tag_manager.create_tag(formatted_date, "master", "Tagged by web scrapper")
            print(f"Tag '{formatted_date}' has been created.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
