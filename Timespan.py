intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        seconds -= value * count
        if value == 1:
            name = name.rstrip("s")
        if value != 0 or len(result) != 0:
            result.append(f"{value}".rjust(2, "0"))
    return ':'.join(result[:granularity])


class Timespan:
    def __init__(self, from_time: float, to_time: float) -> None:
        self.from_time = from_time
        self.to_time = to_time

    def __str__(self) -> str:
        formatted_from_time = display_time(self.from_time * 60)
        formatted_to_time = display_time(self.to_time * 60)
        return f"с {formatted_from_time} до {formatted_to_time}"
