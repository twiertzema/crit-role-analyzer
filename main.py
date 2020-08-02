import json

from functools import reduce

from constants import FIRST_EP, MY_CURRENT_EP


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


def get_total_runtime(episodes, from_episode=FIRST_EP):
    from_index = 0

    for index, episode in enumerate(episodes):
        if episode["href"] == from_episode:
            from_index = index

    return reduce(lambda total, ep: total + ep["runtime"], episodes[from_index:], 0)


def main():
    episodes = load_episodes()
    total_runtime = get_total_runtime(episodes, MY_CURRENT_EP)

    days, hours, minutes, seconds = break_down_time(total_runtime)
    print(f"Total runtime: {days}:{hours}:{minutes}:{seconds}")
    print(f"Gross total: {total_runtime}")


if __name__ == "__main__":
    main()
