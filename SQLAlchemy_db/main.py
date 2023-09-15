import argparse

import handler

FUNCS_DICT = {
    "create": handler.create,
    "update": handler.update,
    "list": handler.list,
    "remove": handler.remove,
}

parser = argparse.ArgumentParser(
    prog="database", description="work with database", epilog="Hello!"
)

parser.add_argument("--action")
parser.add_argument("-m", "--model")
parser.add_argument("--id")
parser.add_argument("-n", "--name")


args = parser.parse_args()
argument_dict = vars(args)


def main(argument_dict):
    try:
        func = argument_dict["action"]
        result = FUNCS_DICT[func](
            name=argument_dict["name"],
            id_=argument_dict["id"],
            model=argument_dict["model"],
        )
        for i in result:
            print(i)

    except Exception as error:
        print(error)


if __name__ == "__main__":
    main(argument_dict)
