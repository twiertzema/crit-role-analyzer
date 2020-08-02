import json

from datetime import datetime
from functools import reduce

from constants import FIRST_EP, MY_CURRENT_EP

MIKE_EP = "/wiki/Stalker_in_the_Swamp"


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


def time_str(time_in_seconds):
    days, hours, minutes, seconds = break_down_time(time_in_seconds)
    return f"{days}:{hours}:{minutes}:{seconds} ({time_in_seconds})"


def get_avg_daily_runtime(episodes, total_runtime):
    first_date = parse_date(episodes[0]["airdate"])
    last_date = parse_date(episodes[-1]["airdate"])
    days_delta = (last_date - first_date).days
    return total_runtime / days_delta


def main():
    episodes = load_episodes()
    no_talks = list(filter(lambda ep: "Talks Machina" not in ep["title"], episodes))

    total_runtime = get_total_runtime(episodes)
    print(f"Gross total: {total_runtime}")
    print(f"Total runtime: {time_str(total_runtime)}")

    total_runtime_no_talks = get_total_runtime(no_talks)
    print(f"Total runtime (no Talks): {time_str(total_runtime_no_talks)}")

    remaining_episodes = episodes_from(episodes, MY_CURRENT_EP)
    remaining_runtime = get_total_runtime(remaining_episodes)
    print(f"Runtime remaining: {time_str(remaining_runtime)}")

    remaining_no_talks_episodes = episodes_from(no_talks, MY_CURRENT_EP)
    remaining_runtime_no_talks = get_total_runtime(remaining_no_talks_episodes)
    print(f"Runtime remaining (no Talks): {time_str(remaining_runtime_no_talks)}")

    print()

    print(
        f"Average (main) episode length: {time_str(total_runtime_no_talks / len(no_talks))}"
    )

    avg_runtime = get_avg_daily_runtime(episodes, total_runtime)
    print(f"Average runtime / week: {break_down_time(avg_runtime * 7)}")

    avg_runtime_no_talks = get_avg_daily_runtime(
        remaining_no_talks_episodes, remaining_runtime_no_talks
    )
    print(
        f"Average runtime / week (no Talks): {break_down_time(avg_runtime_no_talks * 7)}"
    )

    recent_avg_runtime = get_avg_daily_runtime(
        episodes_from(episodes, "/wiki/Talks_Machina_Episode_1"), total_runtime
    )
    print(
        f'Average runtime / week since "Talks": {break_down_time(recent_avg_runtime * 7)}'
    )

    print()

    latest_airdate = parse_date(episodes[-1]["airdate"])
    target_date = datetime(year=2020, month=12, day=31)
    target_diff = (target_date - latest_airdate).days
    print(f"Days remaining until target: {target_diff}")

    print()

    additional_runtime = int(target_diff * recent_avg_runtime)
    total_target_runtime = remaining_runtime + additional_runtime
    print(f"Total runtime until target: {time_str(total_target_runtime)}")

    target_watch_rate = int(total_target_runtime / target_diff)
    print(f"Target watch rate / week: {time_str(target_watch_rate * 7)}")

    print()

    additional_runtime_no_talks = int(target_diff * avg_runtime_no_talks)
    total_target_runtime_no_talks = (
        remaining_runtime_no_talks + additional_runtime_no_talks
    )
    print(
        f"Total runtime until target (no Talks): {time_str(total_target_runtime_no_talks)}"
    )

    target_watch_rate_no_talks = int(total_target_runtime_no_talks / target_diff)
    print(
        f"Target watch rate / week (no Talks): {time_str(target_watch_rate_no_talks * 7)}"
    )


if __name__ == "__main__":
    main()
