#!/usr/bin/env python3
import sys

from ruamel.yaml import YAML
from ruamel.yaml.constructor import ConstructorError


def join_constructor(loader, node):
    parts = loader.construct_sequence(node)
    return "".join(parts)


def main():
    yaml = YAML(typ="safe")
    yaml.Constructor.add_constructor("!join", join_constructor)

    for path in sys.argv[1:]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                yaml.load(f)
        except ConstructorError as e:
            print(f"{path}: YAML constructor error: {e}")
            return 1
        except Exception as e:
            print(f"{path}: YAML syntax error: {e}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
