"""Command-line interface for StructOPE."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="structope",
        description="StructOPE — Off-Policy Evaluation under Structural Shift",
    )
    parser.add_argument("--version", action="store_true", help="print version")
    parser.add_argument("--info", action="store_true", help="print protocol info")
    args = parser.parse_args(argv)

    if args.version:
        from structope import __version__
        print(f"structope {__version__}")
        return 0

    if args.info:
        print("StructOPE v1.0.0 — pre-registered protocol, executed.")
        print("Zenodo:  10.5281/zenodo.24473998")
        print("OSF:     10.17605/OSF.IO/EZJKF")
        print("Figshare: 10.6084/m9.figshare.35117266")
        print("Repo:    https://github.com/gitdeeper16/structope")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
