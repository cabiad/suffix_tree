import unittest

from suffix_tree import SuffixTree


class SuffixTreeTestCase(unittest.TestCase):
    def test_init(self):
        st = SuffixTree('foo')
        rows = st.get_rows()

        self.assertEqual(len(rows), 5)  # root plus len(foo) + null term
        self.assertEqual(len(rows[0]), 1)  # The root level
        self.assertEqual(len(rows[1]), 3)  # 'f', 'o', and '\0'
        self.assertEqual(len(rows[2]), 3)  # 'o' (of f), 'o' (of o),
                                           # '\0' (of o)
        self.assertEqual(len(rows[3]), 2)  # 'o' (of o of f), '\0' (of o of o)
        self.assertEqual(len(rows[4]), 1)  # '\0' (of o)

        root_item = rows[0][0]
        self.assertEqual(root_item.let, None)
        self.assertEqual(root_item.parent, None)
        self.assertEqual(root_item.depth, 0)
        self.assertEqual(root_item.positions, set([None]))

        self.assertIn('f', root_item.children)
        self.assertIn('o', root_item.children)
        self.assertIn("\0", root_item.children)

        f_item = root_item.children['f']
        o_item = root_item.children['o']
        null_item = root_item.children['\0']

        row1 = (f_item, o_item, null_item)

        self.assertEqual([item.let for item in row1], ['f', 'o', '\0'])
        self.assertEqual([item.parent for item in row1], 3 * [rows[0][0], ])
        self.assertEqual([item.depth for item in row1], [1, 1, 1])
        self.assertEqual([item.positions for item in row1],
                         [set([0]), set([1, 2]), set([3])])

        f_child_o = f_item.children['o']
        self.assertEqual(f_child_o.let, 'o')
        self.assertEqual(f_child_o.parent, f_item)
        self.assertEqual(f_child_o.depth, 2)
        self.assertEqual(f_child_o.positions, set([1]))

        o_child_o = o_item.children['o']
        self.assertEqual(o_child_o.let, 'o')
        self.assertEqual(o_child_o.parent, o_item)
        self.assertEqual(o_child_o.depth, 2)
        self.assertEqual(o_child_o.positions, set([2]))

        # FIXME: Comprehensive testing is really called for here. Test every
        # node in the tree.

        lowest_null_parent = f_child_o.children['o']
        lowest_null = lowest_null_parent.children['\0']
        self.assertEqual(lowest_null.let, '\0')
        self.assertEqual(lowest_null.parent, lowest_null_parent)
        self.assertEqual(lowest_null.depth, 4)
        self.assertEqual(lowest_null.positions, set([3]))

    def test_search(self):
        st = SuffixTree('This is a test')
        self.assertEqual(st.search('T'), [0])
        self.assertEqual(st.search('Th'), [0])
        self.assertEqual(st.search('h'), [1])
        self.assertEqual(st.search('is'), [2, 5])
        self.assertEqual(st.search('qqqqq'), None)
