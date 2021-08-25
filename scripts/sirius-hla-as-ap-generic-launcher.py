#!/usr/bin/env python
import argparse
import inspect
import json

from siriushlacon.application import launch_pydm
from siriushlacon.logging import get_logger

logger = get_logger("")
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generic Launcher")
    parser.add_argument(
        "params",
        help=f"json str to be forwarded into `launch_pydm(`{inspect.signature(launch_pydm).__str__()})",
    )
    args = parser.parse_args()
    data = json.loads(args.params)
    logger.info(f"Launch siriushlacon PyDM OPI - {data}")
    launch_pydm(**data)
