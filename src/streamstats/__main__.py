import argparse
import sys
from streamstats.analysis import Statistics
from streamstats.errors import StreamStatsError
from streamstats.parsers import parse_csv, parse_jsonl
from streamstats.report import make_report, save_report
import logging

logging.basicConfig(level=logging.INFO)

def make_arg_parser():
    parser = argparse.ArgumentParser(description="Анализ файлов")
    subparsers = parser.add_subparsers(dest='command', required=True)

    analyze_parser = subparsers.add_parser('analyze', help="Анализ файлов")
    analyze_parser.add_argument("inputs", nargs="+", help="Анализ input файлов")
    analyze_parser.add_argument("--format", choices=['csv', 'jsonl'],
                                required=True, help="Формат input файлов")
    analyze_parser.add_argument("--output", required=True, help="Путь к файлу отчета")
    analyze_parser.add_argument("--skip-invalid", action='store_true')

    return parser



def run_analyze(args):
    statistics = Statistics()

    if args.format == 'csv':
        parse_func = parse_csv

    else:
        parse_func = parse_jsonl

    for input_path in args.inputs:
        events = parse_func(input_path, skip_invalid=args.skip_invalid)

        for event in events:
            if event is None:
                statistics.skip_invalid += 1
                continue
            statistics.add_event(event)

    report = make_report(statistics)
    save_report(report, args.output)


def main():
    parser = make_arg_parser()
    args = parser.parse_args()

    try:
        if args.command == 'analyze':
            run_analyze(args)
    except StreamStatsError as e:
        print(e, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
