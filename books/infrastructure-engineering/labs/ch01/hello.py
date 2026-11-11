import platform


def describe(count):
    match count:
        case 0:
            return "no visitors yet"
        case 1:
            return "one visitor"
        case _:
            return f"{count} visitors"


print(describe(3), "on Python", platform.python_version(), platform.system())
