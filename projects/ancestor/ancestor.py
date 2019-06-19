def earliest_ancestor(lst, n):
    '''
    Accepts a list of relationships as **lst**,
    builds a graph to store the relationships,
    and returns the oldest ancestor of **n**, or -1 if no parent.
    '''
    ships = {}

    for relation in lst:
        if not relation[1] in ships:
            ships[relation[1]] = set()
            
        ships[relation[1]].add(relation[0])

    longest = []

    def traverse(node, path):
        nonlocal longest
        if not node in ships:
            if not path:
                return None
            elif len(path) > len(longest) \
                 or (len(path) == len(longest) and path[-1] < longest[-1]):
                longest = path
            return None

        for i in ships[node]:
            traverse(i, path + [i])
                

    traverse(n, [])
    
    return longest[-1] if longest else -1

#test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
#print(earliest_ancestor(test_ancestors, 3))
