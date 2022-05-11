from collections import namedtuple


def get_toc(doc):
    """ Get a dict representing the Table of Contents for a markdown document.

    Args:
        doc: List of strings, each string is a line from the
            markdown document.

    Returns:
        dict:
            Keys are the markdown heading names
            Values are NamedTuples with the start and end index of each section,
            including any nested subsections. Using the tuple as a slice
            will return the lines of text in the given section.

    Given a markdown document with the following content:
    '''# Python
    ## Lists

    Lists are blah blah blah...

    ## Dicts

    Dicts are blah blah blah...

    ### Types of dict

    Loads actually...
    '''
    The following dict will be returned:
    {
        'Python': (0, 13),
        'Lists': (1, 5),
        'Dicts': (5, 13),
        'Types of dict': (9, 13),
    }
    The Values are NamedTuples with 'start' and 'end' respectively.
    If the returned dict is stored in toc, access the end index of
    the Lists section using `toc['lists'].end`.
    """
    toc = []
    for index, line in enumerate(doc):
        line = line.strip()
        if line.startswith("#"):
            heading = line.split(None, 1)[-1]
            depth = line.index(" ")
            toc.append((heading, depth, index))

    # Process list in reverse order so that when processing each entry you
    # already know the end index for the section.
    toc_dict = {}
    end = {0: len(doc)}

    Section = namedtuple('Section', ['start', 'end'])

    for section in reversed(toc):
        heading = section[0].lower()
        depth = section[1]
        start_index = section[2]

        # Section (start) index is the end index for that depth section or
        # deeper when traversing the sections in reverse.

        # Find the biggest index which is less than or equal to the depth
        end_index = end[max(key for key in end.keys() if key <= depth)]
        #  Set the new end index for sections of this depth
        end[depth] = start_index
        # Remove end indexes greater than the current depth
        end = {k: v for (k, v) in end.items() if k <= depth}
        toc_dict[heading] = Section(start_index, end_index)
    return toc_dict
