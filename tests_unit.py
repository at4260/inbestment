"""
Unittests to check that the results are calculating correctly
based on various user input.

Two main functions are generating the results/priority goals
and associated semi-circle graphs:
utils.calc_financial_results - calculating the "Amount Funded"
utils.calc_max_financials - calculating the "Target Remaining"
"""

import unittest
import utils


class UserResultsTestCase(unittest.TestCase):
    def test_user_results_one(self):
        self.assertEqual(utils.calc_financial_results(
            0, 0, "No", "No", 0, 0), {
            "checking": 0, "savings": 0, "match": 0,
            "ira": 0, "ret401k": 0, "investment": 0})

    def test_user_results_two(self):
        self.assertEqual(utils.calc_financial_results(
            0, 0, "Yes", "Yes", 0, 0), {
            "checking": 0, "savings": 0, "match": 0,
            "ira": 0, "ret401k": 0, "investment": 0})

    def test_user_results_three(self):
        self.assertEqual(utils.calc_financial_results(
            10000, 60000, "No", "No", 0, 0), {
            "checking": 3700, "savings": 6300, "match": 0,
            "ira": 0, "ret401k": 0, "investment": 0})

    def test_user_results_four(self):
        self.assertEqual(utils.calc_financial_results(
            20000, 60000, "No", "No", 0, 0), {
            "checking": 3700, "savings": 11100, "match": 0,
            "ira": 5200, "ret401k": 0, "investment": 0})

    def test_user_results_five(self):
        self.assertEqual(utils.calc_financial_results(
            30000, 60000, "No", "No", 0, 0), {
            "checking": 3700, "savings": 11100, "match": 0,
            "ira": 5500, "ret401k": 0, "investment": 9700})

    def test_user_results_six(self):
        self.assertEqual(utils.calc_financial_results(
            10000, 60000, "Yes", "Yes", 1.0, 0.05), {
            "checking": 3700, "savings": 6300, "match": 0,
            "ira": 0, "ret401k": 0, "investment": 0})

    def test_user_results_seven(self):
        self.assertEqual(utils.calc_financial_results(
            20000, 60000, "Yes", "Yes", 1.0, 0.05), {
            "checking": 3700, "savings": 11100, "match": 3000,
            "ira": 2200, "ret401k": 0, "investment": 0})

    def test_user_results_eight(self):
        self.assertEqual(utils.calc_financial_results(
            30000, 60000, "Yes", "Yes", 1.0, 0.05), {
            "checking": 3700, "savings": 11100, "match": 3000,
            "ira": 5500, "ret401k": 6700, "investment": 0})

    def test_user_results_eight(self):
        self.assertEqual(utils.calc_financial_results(
            40000, 60000, "Yes", "Yes", 1.0, 0.05), {
            "checking": 3700, "savings": 11100, "match": 3000,
            "ira": 5500, "ret401k": 15000, "investment": 1700})

    def test_user_results_nine(self):
        self.assertEqual(utils.calc_financial_results(
            10000, 60000, "Yes", "No", 0, 0), {
            "checking": 3700, "savings": 6300, "match": 0,
            "ira": 0, "ret401k": 0, "investment": 0})

    def test_user_results_ten(self):
        self.assertEqual(utils.calc_financial_results(
            20000, 60000, "Yes", "No", 0, 0), {
            "checking": 3700, "savings": 11100, "match": 0,
            "ira": 5200, "ret401k": 0, "investment": 0})

    def test_user_results_eleven(self):
        self.assertEqual(utils.calc_financial_results(
            30000, 60000, "Yes", "No", 0, 0), {
            "checking": 3700, "savings": 11100, "match": 0,
            "ira": 5500, "ret401k": 9700, "investment": 0})

    def test_user_results_twelve(self):
        self.assertEqual(utils.calc_financial_results(
            40000, 60000, "Yes", "No", 0, 0), {
            "checking": 3700, "savings": 11100, "match": 0,
            "ira": 5500, "ret401k": 18000, "investment": 1700})


class MaxResultsTestCase(unittest.TestCase):
    def test_max_results_one(self):
        self.assertEqual(utils.calc_max_financials(
            0, "No", "No", 0, 0), {
            "checking": 0, "savings": 0, "match": 0,
            "ira": 5500, "ret401k": 0, "investment": 0})

    def test_max_results_two(self):
        self.assertEqual(utils.calc_max_financials(
            0, "Yes", "Yes", 0, 0), {
            "checking": 0, "savings": 0, "match": 0,
            "ira": 5500, "ret401k": 18000, "investment": 0})

    def test_max_results_three(self):
        self.assertEqual(utils.calc_max_financials(
            0, "Yes", "No", 0, 0), {
            "checking": 0, "savings": 0, "match": 0,
            "ira": 5500, "ret401k": 18000, "investment": 0})

    def test_max_results_four(self):
        self.assertEqual(utils.calc_max_financials(
            60000, "No", "No", 0, 0), {
            "checking": 3700, "savings": 11100, "match": 0,
            "ira": 5500, "ret401k": 0, "investment": 0})

    def test_max_results_five(self):
        self.assertEqual(utils.calc_max_financials(
            60000, "Yes", "No", 0, 0), {
            "checking": 3700, "savings": 11100, "match": 0,
            "ira": 5500, "ret401k": 18000, "investment": 0})

    def test_max_results_six(self):
        self.assertEqual(utils.calc_max_financials(
            60000, "Yes", "Yes", 1.0, 0.05), {
            "checking": 3700, "savings": 11100, "match": 3000,
            "ira": 5500, "ret401k": 15000, "investment": 0})


if __name__ == "__main__":
    unittest.main()
