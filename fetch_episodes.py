import bs4
import json
import requests

from constants import BASE_URL, FIRST_EP


def update_episodes(episodes, new_ep):
    for i, ep in enumerate(episodes):
        if ep["href"] == new_ep["href"]:
            episodes[i] = new_ep
            return episodes

    episodes.append(new_ep)
    return episodes


def parse_time(time_str):
    time_parts = [int(x) for x in time_str.split(":")]

    if len(time_parts) == 2:
        hours = 0
        minutes, seconds = time_parts
    else:
        hours, minutes, seconds = time_parts

    return hours * 3600 + minutes * 60 + seconds


def gen_episodes(from_episode=FIRST_EP):
    episode_path = from_episode

    while True:
        print(f"Requesting {episode_path}...")
        res = requests.get(BASE_URL.format(episode_path))
        soup = bs4.BeautifulSoup(res.text, "lxml")

        episode = {
            "title": soup.select(".pi-title")[0].text,
            "airdate": soup.select("[data-source='Airdate'] > .pi-data-value")[0].text,
            "href": episode_path,
        }

        try:
            episode["runtime"] = parse_time(
                soup.select("[data-source='Runtime'] > .pi-data-value")[0].text
            )
        except ValueError:
            episode["runtime"] = 0

        try:
            episode["next_href"] = soup.select(
                "tbody [data-source='NextAirdateEp'] > a"
            )[0]["href"]
            episode_path = episode["next_href"]
            yield episode
        except KeyError:
            print("Reached the latest episode")
            yield episode
            break


def fetch_episodes():
    episodes = []

    with open("db\\episodes.json", mode="r") as f:
        episodes += json.loads(f.read())

    starting_episode = episodes[-2]["next_href"]

    for episode in gen_episodes(starting_episode):
        episodes = update_episodes(episodes, episode)

        with open("db\\episodes.json", mode="w") as f:
            f.write(json.dumps(episodes, indent=2))
