import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse


class DateExtractor:
    def __init__(self, url, search_key, search_value):
        self.url = url
        self.search_key = search_key
        self.search_value = search_value

    def fetch_date(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            start = text.find(self.search_key) + len(self.search_key)
            end = text.find(self.search_value, start)
            date_edition = text[start:end].strip()
            return date_edition
        else:
            raise Exception(
                f"Failed to retrieve the website. Status code: {response.status_code}"
            )


class DateFormatter:
    @staticmethod
    def format_date(date_str):
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            raise Exception(f"Failed to parse the date: {date_str}")


class GitLabTagManager:
    def __init__(self, project_id, private_token):
        self.gitlab_api_url = "https://gitlab.com/api/v4"
        self.project_id = project_id
        self.private_token = private_token

    def tag_exists(self, tag_name):
        check_tag_url = (
            f"{self.gitlab_api_url}/projects/{self.project_id}/repository/tags/{tag_name}"
        )
        headers = {"PRIVATE-TOKEN": self.private_token}
        response = requests.get(check_tag_url, headers=headers)
        return response.status_code == 200

    def create_tag(self, tag_name, ref, message):
        create_tag_url = (
            f"{self.gitlab_api_url}/projects/{self.project_id}/repository/tags"
        )
        tag_data = {
            "tag_name": tag_name,
            "ref": ref,
            "message": message,
        }
        headers = {"PRIVATE-TOKEN": self.private_token}
        response = requests.post(create_tag_url, headers=headers, data=tag_data)
        if response.status_code != 201:
            raise Exception(
                f"Failed to create tag. Status code: {response.status_code}, Response: {response.text}"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Extract date from a webpage and create a GitLab tag."
    )
    parser.add_argument(
        "--qnx71release_info_url",
        required=True,
        help="URL of the webpage to extract date from",
    )
    parser.add_argument("--project_id", required=True, help="GitLab project ID")
    parser.add_argument("--private_token", required=True, help="GitLab private token")
    parser.add_argument(
        "--search_key", required=True, help="Key text to search for date extraction"
    )
    parser.add_argument(
        "--search_value", required=True, help="Value text to end date extraction"
    )

    args = parser.parse_args()

    url = args.qnx71release_info_url
    project_id = args.project_id
    private_token = args.private_token
    search_key = args.search_key
    search_value = args.search_value

    date_extractor = DateExtractor(url, search_key, search_value)
    date_edition = date_extractor.fetch_date()

    date_formatter = DateFormatter()
    formatted_date = date_formatter.format_date(date_edition)

    gitlab_tag_manager = GitLabTagManager(project_id, private_token)

    if gitlab_tag_manager.tag_exists(formatted_date):
        print(f"Tag '{formatted_date}' already exists.")
    else:
        gitlab_tag_manager.create_tag(
            formatted_date, "master", f"Tag created for edition date {date_edition}"
        )
        print(f"Tag '{formatted_date}' created successfully.")


if __name__ == "__main__":
    main()
