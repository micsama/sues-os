import sys


def lower_json(json_info):
    if isinstance(json_info, dict):
        for key in list(json_info.keys()):
            if key.islower():
                lower_json(json_info[key])
            else:
                key_lower = key.lower()
                json_info[key_lower] = json_info[key]
                del json_info[key]
                lower_json(json_info[key_lower])

    elif isinstance(json_info, list):
        for item in json_info:
            lower_json(item)


def getStartArgs(count: int) -> list:
    res = []
    for c in range(count):
        res.append(sys.argv[c + 1])
    return res


def argsCount() -> int:
    return len(sys.argv) - 1


if __name__ == "__main__":
    1
