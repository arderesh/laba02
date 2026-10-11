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
    parser = argparse.ArgumentParser(description="Анализ файлов")
    subarsers = parser.add_subparsers(dest='command', required=True)

    analize_parser = subarsers.add_parser('analize', help="Анализ файлов")
    analize_parser.add_argument("inputs", nargs="+", help="Анализ input файлов")
    analize_parser.add_argument("--format", choices=['csv', 'jsonl'], required=True, help="Формат input файлов")
    analize_parser.add_argument("--output", required=True, help="Путь к файлу отчета")
    analize_parser.add_argument("--skip-invalid", action='store_true')

    return parser


def run_analize(args):
    statistics = Statistics()

    if args.format == 'csv':
        parse_func = parse_csv

    else:
        parse_func = parse_jsonl

    for input_path in args.inputs:
        events = parse_func(input_path)

        for event in events:
            statistics.add_event(event)

    report = make_report(statistics)
    save_report(report, args.output)


def main():
    parser = make_arg_parser()
    args = parser.parse_args()

    try:
        if args.command == 'analize':
            run_analize(args)
    except StreamStatsError as e:
        print(e, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())