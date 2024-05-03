def lst_to_str(lst: list) -> str:
    """
    Convert a list of elements to a string representation.

    Args:
        lst (list): The list of elements to be converted to a string.

    Returns:
        str: A string representation of the input list with elements enclosed 
             in parentheses and separated by commas.

    Examples:
        >>> lst_to_str([40, 41, 31, 43, 20, 23, 38])
        '(40, 41, 31, 43, 20, 23, 38)'
        >>> lst_to_str(['apple', 'banana', 'cherry'])
        "('apple', 'banana', 'cherry')"
        >>> lst_to_str([])
        '()'

    Note:
        - If the input list is empty, an empty string with parentheses '()' 
          will be returned.
        - Elements in the list will be converted to their string 
          representations using the str() function.
    """
    return '(' + ', '.join(map(str, lst)) + ')'
