import requests

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
