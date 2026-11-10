"""shelf search TEXT"""

from __future__ import annotations

import argparse
import unicodedata

from shelf.store import Store


def register(subparsers) -> None:
    parser = subparsers.add_parser("search", help="find books by title or author")
    parser.add_argument("text", metavar="TEXT", help="text to look for, ignoring case")
    parser.set_defaults(handler=run)


def normalize(text: str) -> str:
    """Fold case and compose accents, so 'GARCÍA' and 'García' compare equal."""
    return unicodedata.normalize("NFC", text.casefold())


def run(args: argparse.Namespace, store: Store) -> int:
    needle = normalize(args.text)
    matches = [
        book
        for book in store.load()
        if needle in normalize(book.title) or needle in normalize(book.author)
    ]
    if not matches:
        print(f'No books match "{args.text}".')
        return 0
    for book in matches:
        print(book)
    return 0
