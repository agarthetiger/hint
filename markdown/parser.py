def get_toc(doc):
    """ Get a dict representing the Table of Contents for a markdown document.

    Args:
        doc: List of strings, each string is a line from the
            markdown document.

    Returns:
        dict:
            Keys are the section heading names
            Values are Tuples with the start and end index of each section,
                including any nested subsections.
    """
    toc = []
    for index, line in enumerate(doc):
        if line.startswith("#"):
            heading = line.split(None, 1)[-1]
            depth = line.index(" ")
            toc.append((heading, depth, index))

    # Process list in reverse order so that when processing each entry you
    # already know the end index for the section.
    toc_dict = {}
    end = {0: len(doc)}

    for section in reversed(toc):
        heading = section[0]
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
        toc_dict[heading] = (start_index, end_index)
    return toc_dict
