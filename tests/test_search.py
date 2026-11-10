from tests.support import ShelfTestCase


class SearchCommandTest(ShelfTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.shelf("add", "Dune", "Frank Herbert")
        self.shelf("add", "One Hundred Years of Solitude", "Gabriel García Márquez")
        self.shelf("add", "Children of Dune", "Frank Herbert", "--status", "reading")

    def test_a_title_match(self):
        result = self.shelf("search", "solitude")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "#2 [to-read] One Hundred Years of Solitude by Gabriel García Márquez\n",
        )

    def test_an_author_match_lists_every_book_in_id_order(self):
        result = self.shelf("search", "herbert")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "#1 [to-read] Dune by Frank Herbert",
            "#3 [reading] Children of Dune by Frank Herbert",
        ])

    def test_matching_ignores_case_including_accented_letters(self):
        result = self.shelf("search", "GARCÍA")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "#2 [to-read] One Hundred Years of Solitude by Gabriel García Márquez\n",
        )

    def test_composed_and_decomposed_accents_match(self):
        decomposed = "García"  # "i" followed by a combining acute accent

        result = self.shelf("search", decomposed)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("#2 ", result.stdout)

    def test_no_match_says_so_and_succeeds(self):
        result = self.shelf("search", "Tolkien")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'No books match "Tolkien".\n')

    def test_search_without_text_is_a_usage_error(self):
        result = self.shelf("search")

        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: shelf search", result.stderr)

    def test_search_does_not_modify_the_shelf_file(self):
        before = self.shelf_path.read_bytes()
        modified = self.shelf_path.stat().st_mtime_ns

        self.shelf("search", "Dune")
        self.shelf("search", "Tolkien")

        self.assertEqual(self.shelf_path.read_bytes(), before)
        self.assertEqual(self.shelf_path.stat().st_mtime_ns, modified)
