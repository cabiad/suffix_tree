####################################
# Copyright Christopher Abiad, 2013
# All Rights Reserved
####################################
"""Suffix tree implementation created for personal study and
experimentation.

Suffix trees are a data structure to store pre-processed bodies of
text such that we can quickly determine all locations of an arbitrary
query string within.

In short, suffix trees operate on the principal that any query string
that exists within the body of text is the prefix of some suffix (!).

Suffix trees are related to suffix arrays, which provide most of the
same abilities but are more memory efficient.

This implementation is inefficient, requiring both O(n**2) time and space
to generate. It also makes some naive assumptions about the data,
including that only a single letter will ever be passed and that the
body of text we are indexing does not contain the character '\0'.

O(n) space is achevable by storing the original string in
an array and compressing non-branching parts of the tree to a single
node. Clever algorithms exist for O(n) time as well, but these have not
yet been implemented.
"""

__author__ = 'Christopher Abiad'


class SuffixTree(object):

    class Node(object):
        def __init__(self, let, strpos, parent):
            self.let = let

            if strpos is not None:
                strpos = int(strpos)
            self.positions = set([strpos, ])

            self.parent = parent
            if parent is None:
                self.depth = 0
            else:
                self.depth = parent.depth + 1

            self.children = {}

        def add_child(self, let, strpos):
            child = self.children.get(let, None)
            # If the child already exists, add this occurrence to it
            if child is not None:
                child.positions.add(strpos)
                return child
            child = SuffixTree.Node(let, strpos, self)
            self.children[let] = child
            return child

        def has_child(self, let):
            return let in [n.let for n in self.children.values()]

        def __repr__(self):
            return "<Node at {i}>('{l}', {pos}, {parent})\t".format(
                i=str(id(self)),
                l=self.let,
                pos=str(self.positions),
                parent=str(id(self.parent))
            )

    class BreadthFirstIterator(object):
        def __init__(self, tree):
            self.queue = [tree.root, ]

        def __iter__(self):
            return self

        def next(self):
            # dequeue head of list and store. If no items left, we are done
            try:
                node = self.queue.pop(0)
                #print 'n' + str(node)
            except IndexError:
                raise StopIteration

            # enqueue head's child nodes
            for child in node.children.values():
                self.queue.append(child)

            return node

    def __init__(self, text):
        # Root node has no letter, parent, or strpos, it stores None
        # for all of these instead. It simply serves to link to child
        # nodes
        self.root = SuffixTree.Node(None, None, None)

        # Insert all suffixes of text. Ensure that we always insert the null
        # string too.
        for i in xrange(len(text) + 1):
            #print text[i:]
            self.insert(text[i:], _shift=i)

        self._compact()

    def _compact(self):
        pass

    def insert(self, word, _shift=0):
        """Add word to tree structure
        """
        cur = self.root
        for i, let in enumerate(word):
            #print 'cur: {c}'.format(c=str(cur))
            #print 'let: {l}'.format(l=let)
            cur = cur.add_child(let, i + _shift)

        cur.add_child("\0", len(word) + _shift)

    def search(self, q):
        cur = self.root

        for l in q:
            try:
                cur = cur.children[l]
            except KeyError:
                return None

        # cur.positions is now set to the positions of the last character
        # in the search string. The user probably wanted the positions of
        # the first character of their query string, so shift it.
        return map(lambda x: x - len(q) + 1, cur.positions)

    def get_rows(self):
        it = SuffixTree.BreadthFirstIterator(self)
        dep = 0
        r = [[]]
        for n in it:
            if n.depth == dep:
                r[dep].append(n)
            else:
                dep += 1
                r.append([n])

        return r

    def __repr__(self):
        it = SuffixTree.BreadthFirstIterator(self)
        dep = 0
        s = ''
        for n in it:
            #print s
            if n.depth == dep:
                if n.parent is None:
                    s = s + "({i}, {l}, None)\t".format(
                        i=str(id(n)), l=n.let)
                else:
                    s = s + "({i}, {l}, {p})\t".format(
                        i=str(id(n)), l=n.let, p=str(id(n.parent)))
            else:
                dep += 1
                s = s + "\n({i}, {l}, {p})\t".format(
                    i=str(id(n)), l=n.let, p=str(id(n.parent)))

        return s
