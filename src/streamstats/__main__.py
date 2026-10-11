import argparse
import logging
import sys
from streamstats.analysis import Statistics
from streamstats.errors import StreamStatsError
from streamstats.parsers import parse_csv, parse_jsonl
from streamstats.report import make_report, save_report


def get_parser(format):
    if format == 'csv':
        return parse_csv

    if format == 'json':
        return parse_jsonl

    raise ValueError('Неподдерживаемый формат')


def make_arg_parser():
    parser = argparse.ArgumentParser()
    subarsers = parser.add_subparsers()

    analize_parser = subarsers.add_parser('analize')
    analize_parser.add_argument("inputs", nargs="+")
    analize_parser.add_argument("--format", choices=['csv', 'jsonl'], reauired=True)
    analize_parser.add_argument("--output", required=True)
    analize_parser.add_argument("--skip-invalid", action='store_true')

    return parser
