#!/usr/bin/env python
from spf.mr.language.type_.term_type import TermType
from spf.mr.language.type_.complex_type import ComplexType
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.unittest.test_services import TestServices
import unittest


class LogicalConstantTest(unittest.TestCase):
    def setUp(self):
        TestServices()

    def test_1(self):
        expr = TestServices.CATEGORY_SERVICES.parse_semantics("boo:e")
        self.assertEqual(expr.__class__, LogicalConstant)
        self.assertEqual(expr.get_type().__class__, TermType)

    def test_2(self):
        expr = TestServices.CATEGORY_SERVICES.parse_semantics("capital:<c,t>")
        self.assertEqual(expr.__class__, LogicalConstant)
        self.assertEqual(expr.get_type().__class__, ComplexType)

if __name__ == "__main__":
    unittest.main()
