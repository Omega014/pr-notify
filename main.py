import config as cf


def check_approved(repository, pr_number):
    """ クソコードやばいので修正したい
    """
    rewiews = requests.get("{api_url}/{repository}/pulls/{number}/reviews?access_token={access_token}&state=open".format(api_url=cf.GITHUB_API_URL, repository=repository, number=pr_number, access_token=cf.GITHUB_ACCESS_TOKEN))
    user_action = {"approved":[], "commented":[]}
    result = ""
    for data in rewiews.json():
        username = data["user"]["login"]
        if data["state"] == "APPROVED":
            if username not in user_action["approved"]:
                user_action["approved"].append(username)
        if data["state"] == "COMMENTED":
            if username not in user_action["commented"]:
                user_action["commented"].append(username)
    for action, username_list in user_action.items():
        for name in username_list:
            if action == "approved":
                result += ":white_check_mark: " + name
            if action == "commented":
                result += ":speech_balloon: " + name
    return result


def check_pull_request(repository, pulls, label):
    text = ""
    count = 0
    for pull in pulls.json():
        if label in [label["name"] for label in pull["labels"]]:
            reviewer_action =  check_approved(repository, pull["number"])
            if reviewer_action:
                text += "- {title}: {url} \n　{action}\n".format(title=pull["title"], url=pull["html_url"], action=reviewer_action)
            else:
                text += "- {title}: {url}\n".format(title=pull["title"], url=pull["html_url"])
            count += 1
    if count == 0:
        output_text = "(0件): \n"
    else:
        output_text = "({}件): \n {}".format(count, text)

    return output_text


def get_post_text(repository):
    pulls = requests.get("{}/{}/pulls?access_token={}&state=open".format(cf.GITHUB_API_URL, repository, cf.GITHUB_ACCESS_TOKEN))
    post_text = """*[{}]*\nレビュー依頼 {}\nレビューされたPR {}\n""".format(repository,
                                                                            check_pull_request(repository, pulls, "review request"),
                                                                            check_pull_request(repository, pulls, "reviewed"))
    return post_text


def main():
    """ PRの状態を確認するbotくんの仕事内容
    """
    post_text = "<!here>\n"
    for repository in cf.REPOSITORY_LIST:
        post_text += get_post_text(repository)

    slack_post_data = {"token": cf.SLACK_ACCESS_TOKEN,
                       "channel": cf.CHANNEL,
                       "username": cf.BOT_USER_NAME,
                       "pretext": "<!here>\n",
                       "text": post_text,
                       "icon_emoji": ':fish:',
                       "color": "good"}

    requests.post("https://slack.com/api/chat.postMessage", data=slack_post_data)


if __name__ == '__main__':
    main()
