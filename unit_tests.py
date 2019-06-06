import unittest
from sheet import Sheet


class TestAll(unittest.TestCase):

    sheet = Sheet("test")

    def test_vote(self):
        digit = self.sheet.sheet.cell(2, 3).value
        self.sheet.vote(1, 1)
        digit_after_vote = self.sheet.sheet.cell(2, 3).value
        self.assertTrue(int(digit_after_vote) - int(digit) == 1)

    def test_unvote(self):
        digit = self.sheet.sheet.cell(2, 3).value
        self.sheet.unvote(1, 1)
        digit_after_vote = self.sheet.sheet.cell(2, 3).value
        self.assertTrue(int(digit_after_vote) - int(digit) == -1)


if __name__ == '__main__':
    unittest.main()