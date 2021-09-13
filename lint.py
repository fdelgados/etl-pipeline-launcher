#!/usr/bin/env python

import argparse
import logging
from pylint.lint import Run

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

parser = argparse.ArgumentParser(prog="LINT")

parser.add_argument(
    "-p",
    "--path",
    nargs="+",
    help=(
        "path to directory you want to run pylint | "
        "Default: %(default)s | "
        "Type: %(type)s "
    ),
    default="./",
)

parser.add_argument(
    "-t",
    "--threshold",
    help=(
        "score threshold to fail pylint runner | "
        "Default: %(default)s | "
        "Type: %(type)s "
    ),
    default=7,
    type=float,
)

args = parser.parse_args()
path = list(args.path)
threshold = float(args.threshold)

logger.info(
    "PyLint Starting | Path: {} | Threshold: {} ".format(" ".join(path), threshold)
)

results = Run(path, do_exit=False)

final_score = results.linter.stats["global_note"]

if final_score < threshold:

    message = (
        "PyLint Failed | "
        "Score: {} | "
        "Threshold: {} ".format(final_score, threshold)
    )

    logger.error(message)
    raise Exception(message)

else:
    message = (
        "PyLint Passed | "
        "Score: {} | "
        "Threshold: {} ".format(final_score, threshold)
    )

    logger.info(message)

    exit(0)
