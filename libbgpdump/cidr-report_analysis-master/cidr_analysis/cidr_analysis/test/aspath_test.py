#!/usr/bin/env python2.6

import unittest
from cidr_analysis import aspath

class RemovePrivateConfedPaths(unittest.TestCase):

    def test_private_as_confed_seq(self):
        # from rib.20091016.0000.txt
        self.assertEqual(['13237', '13101', '8495', '8495', '8495', '196624'],
            aspath.remove_private_confed_paths(
            '13237 (64600) 13101 8495 8495 8495 196624'.split()))
        self.assertEqual(['13237', '20485', '41209', '196673'],
            aspath.remove_private_confed_paths(
            '13237 (64600 65033 65044) 20485 41209 196673'.split()))
        self.assertEqual(['13237', '20485', '29049', '196821'],
            aspath.remove_private_confed_paths(
            '13237 (64600 65044) 20485 29049 196821'.split()))

    def test_private_as_confed_set(self):
        # based on test_private_as_confed_seq examples
        self.assertEqual(['13237', '13101', '8495', '8495', '8495', '196624'],
            aspath.remove_private_confed_paths(
            '13237 [64600] 13101 8495 8495 8495 196624'.split()))
        self.assertEqual(['13237', '20485', '41209', '196673'],
            aspath.remove_private_confed_paths(
            '13237 [64600,65033,65044] 20485 41209 196673'.split()))
        self.assertEqual(['13237', '20485', '29049', '196821'],
            aspath.remove_private_confed_paths(
            '13237 [64600,65044] 20485 29049 196821'.split()))

    def test_non_private_confed_seq(self):
        # based on test_private_as_confed_seq examples
        self.assertEqual(
            ['13237', '13101', '(8495)', '8495', '8495', '196624'],
            aspath.remove_private_confed_paths(
            '13237 (64600) 13101 (8495) 8495 8495 196624'.split()))
        self.assertEqual(
            ['13237', '(64600', '3', '65044)', '20485', '41209', '196673'], aspath.remove_private_confed_paths(
            '13237 (64600 3 65044) 20485 41209 196673'.split()))
        self.assertEqual(
            ['13237', '(64600', '3356)', '20485', '29049', '196821'],
            aspath.remove_private_confed_paths(
            '13237 (64600 3356) 20485 29049 196821'.split()))

    def test_non_private_confed_set(self):
        # based on test_private_as_confed_seq examples
        self.assertEqual(
            ['13237', '13101', '[3]', '8495', '8495', '196624'],
            aspath.remove_private_confed_paths(
            '13237 [64600] 13101 [3] 8495 8495 196624'.split()))
        self.assertEqual(
            ['13237', '[64600,3,65044]', '20485', '41209', '196673'], aspath.remove_private_confed_paths(
            '13237 [64600,3,65044] 20485 41209 196673'.split()))
        self.assertEqual(
            ['13237', '[64600,3356]', '20485', '29049', '196821'],
            aspath.remove_private_confed_paths(
            '13237 [64600,3356] 20485 29049 196821'.split()))

    def test_mixed_seq_set(self):
        # based on test_private_as_confed_seq examples
        self.assertEqual(['13237', '20485', '41209', '196673'],
            aspath.remove_private_confed_paths(
            '13237 (64600 65033 65044) 20485 [65000] 41209 196673'.split()))
        self.assertEqual(['13237', '20485', '29049', '196821'],
            aspath.remove_private_confed_paths(
            '13237 (64600 65044) 20485 29049 [65000,65001] 196821'.split()))


class TestExtractASN(unittest.TestCase):

    def test_illegal_brackets(self):
        self.assertRaises(ValueError, aspath.extract_asn, '(123,345)')
        self.assertRaises(ValueError, aspath.extract_asn, '[123,345]')

    def test_illegal_string(self):
        self.assertRaises(ValueError, aspath.extract_asn, '123 {345,456}')
        self.assertRaises(ValueError, aspath.extract_asn, '123i')

    def test_valid_single_as(self):
        self.assertEqual(123, aspath.extract_asn('123'))
        self.assertEqual(123, aspath.extract_asn(' 123 '))
        self.assertEqual(345, aspath.extract_asn('{345}'))
        self.assertEqual(345, aspath.extract_asn('{ 345 }'))

    def test_multiple_as_set(self):
        self.assertEqual(-1, aspath.extract_asn('{123,345}'))
        self.assertEqual(-1, aspath.extract_asn('{123, 345}'))


class TestDeprependASPath(unittest.TestCase):

    def test_prepended(self):
        self.assertEqual([1], aspath.deprepend_as_path([1]*100))
        self.assertEqual([1, 2, 3, 4, 5],
            aspath.deprepend_as_path([1, 1, 2, 3, 3, 4, 5, 5]))
        self.assertEqual([1, 2, 3, 1, 2, 1],
            aspath.deprepend_as_path([1, 1, 2, 3, 3, 1, 1, 1, 2, 1]))

    def test_unprepended(self):
        path = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(path, aspath.deprepend_as_path(path))


class TestDeloopASPath(unittest.TestCase):

    def test_nonloops(self):
        path = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(path, aspath.deloop_as_path(path))

    def test_simple_loops(self):
        # from straightenRV manpage
        self.assertEqual([1, 2, 5], aspath.deloop_as_path([1, 2, 3, 2, 5]))

    def test_complex_loops(self):
        # from straightenRV manpage
        self.assertEqual(None, aspath.deloop_as_path([1, 2, 3, 2, 3, 4]))
        self.assertEqual(None, aspath.deloop_as_path([1, 2, 3, 2, 4, 5, 4]))


class TestNormalizeASPath(unittest.TestCase):

    def test_private_asns(self):
        path = ['1', '65535', '2', '{65400}', '65000', '{3}']
        norm_path = [1, 2, 3]
        self.assertEqual(norm_path, aspath.normalize_as_path(path))

    def test_straightenrv_example(self):
        # from straightenRV code comment
        path = ['0', '4006', '209', '15254', '15251', '15254', '15254',
            '15254', '15254']
        norm_path = [0, 4006, 209, 15254]
        self.assertEqual(norm_path, aspath.normalize_as_path(path))

    def test_composed_cases(self):
        path = ['1','1','{1}', '2', '3', '3', '2', '3', '{2}', '{2,3}']
        norm_path = [1, 2, -1]
        self.assertEqual(norm_path, aspath.normalize_as_path(path))
        path = ['1','1','{1}', '2', '3', '3', '2', '3', '{3}', '{2,3}']
        norm_path = None
        self.assertEqual(norm_path, aspath.normalize_as_path(path))
        path = ['{2,3}', '{3,4}', '{4,5}', '{5,6}']
        norm_path = [-1]
        self.assertEqual(norm_path, aspath.normalize_as_path(path))
        # confed_set & confed_seq
        path = ['1','1','{1}', '2', '3', '3', '(65000', '65001)', '2']
        norm_path = [1, 2]
        self.assertEqual(norm_path, aspath.normalize_as_path(path))
        path = ['1','1','{1}', '2', '3', '3', '(6500', '6501)', '2']
        norm_path = None
        self.assertRaises(ValueError, aspath.normalize_as_path, path)
