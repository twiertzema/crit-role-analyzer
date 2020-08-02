import json

from datetime import datetime
from functools import reduce

from constants import FIRST_EP, MY_CURRENT_EP


def episodes_from(episodes, from_episode: str):
    from_index = 0

    for index, episode in enumerate(episodes):
        if episode["href"] == from_episode:
            from_index = index

    return episodes[from_index:]


def episodes_to(episodes, to_episode: str):
    result = []

    for episode in episodes:
        if episode["href"] == to_episode:
            break
        result.append(episode)

    return result


def load_episodes():
    with open("db\\episodes.json", mode="r") as f:
        return json.loads(f.read())


def break_down_time(time_in_seconds):
    days = int(time_in_seconds / 86400)
    leftover = time_in_seconds % 86400

    hours = int(leftover / 3600)
    leftover = leftover % 3600

    minutes = int(leftover / 60)
    seconds = leftover % 60

    return days, hours, minutes, seconds


def get_total_runtime(episodes):
    return reduce(lambda total, ep: total + ep["runtime"], episodes, 0)


def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str.split(" ")[0], "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str.split(" ")[0], "%d-%m-%Y")
        except ValueError:
            return datetime.strptime(date_str.split(" ")[0], "%m-%d-%Y")


def get_avg_daily_runtime(episodes, total_runtime):
    first_date = parse_date(episodes[0]["airdate"])
    last_date = parse_date(episodes[-1]["airdate"])
    days_delta = (last_date - first_date).days
    return total_runtime / days_delta


def main():
    episodes = load_episodes()

    total_runtime = get_total_runtime(episodes)
    days, hours, minutes, seconds = break_down_time(total_runtime)
    print(f"Total runtime: {days}:{hours}:{minutes}:{seconds}")
    print(f"Gross total: {total_runtime}")
    print()

    avg_runtime = get_avg_daily_runtime(episodes, total_runtime)
    print(f"Average runtime / week: {break_down_time(avg_runtime * 7)}")

    avg_runtime = get_avg_daily_runtime(
        episodes_from(episodes, "/wiki/Talks_Machina_Episode_1"), total_runtime
    )
    print(f'Average runtime / week since "Talks": {break_down_time(avg_runtime * 7)}')


if __name__ == "__main__":
    main()
