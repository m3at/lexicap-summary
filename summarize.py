#!/usr/bin/env python3

import argparse
import logging

from bs4 import BeautifulSoup
from transformers import pipeline

logger = logging.getLogger("base")


def main() -> None:
    logger.debug("Getting text")
    with open("./transcript.html") as f:
        lines = "".join(f.readlines())
    soup = BeautifulSoup(lines, "html.parser")
    soup.find_all("div", {"class": "t"})
    content = [x.text.lstrip() for x in soup.find_all("div", {"class": "t"})]

    max_size = 64
    hard_max_char = 4000
    l = len(content)
    to_process = []
    for start, end in zip(range(0, l, max_size), range(max_size, l, max_size)):
        to_process.append(" ".join(content[start:end])[:hard_max_char])

    logger.debug("Preparing model")
    # if torch.backends.mps.is_available():
    #     device = torch.device("mps")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # summarizer = pipeline("summarization", model="sshleifer/distilbart-xsum-12-1")

    logger.debug("Summarizing...")
    s = summarizer(to_process, max_length=130, min_length=30, do_sample=False)
    longer_summary = "\n".join(x["summary_text"] for x in s)
    logger.info(f"Summary:\n\n{longer_summary}")

    logger.info("Summary of summary, in a sketchy way")
    sumsum = summarizer(longer_summary[:4000], max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
    logger.info(f"Summary of summary:\n\n{sumsum}")


if __name__ == "__main__":
    # Get system arguments
    parser = argparse.ArgumentParser(
        description="Summarize the content of a Lexicap page",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--log_level",
        type=str,
        default="DEBUG",
        choices=["debug", "info", "warning", "error"],
        help="Logging level",
    )
    args = vars(parser.parse_args())
    log_level = getattr(logging, args.pop("log_level").upper())

    # Setup logging
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter("{asctime} │ {message}", datefmt="%H:%M:%S", style="{"))
    logger.addHandler(ch)

    # Add colors
    _levels = [[226, "DEBUG"], [148, "INFO"], [208, "WARNING"], [197, "ERROR"]]
    for color, lvl in _levels:
        _l = getattr(logging, lvl)
        logging.addLevelName(_l, "\x1b[38;5;{}m{:<7}\x1b[0m".format(color, logging.getLevelName(_l)))

    main()
