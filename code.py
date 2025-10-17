"""
This module provides functions for comparing two text files line by line
and formatting their differences.
"""

def get_file_lines(filename):
    """
    Reads a file and returns its lines as a list of strings.
    Each line is stripped of its trailing newline character.

    Args:
        filename (str): The path to the file.

    Returns:
        list: A list of strings, where each string is a line from the file.
              Returns an empty list if the file cannot be found or read.
    """
    try:
        # 'with open' ensures the file is automatically closed even if errors occur.
        with open(filename, 'r', encoding='utf-8') as file_handle:
            # Read all lines into a list and strip the trailing newline from each.
            lines = [line.rstrip('\n') for line in file_handle.readlines()]
            return lines
    except (FileNotFoundError, IOError):
        # It's often fine to catch multiple related exceptions together.
        return []

def singleline_diff(line1, line2):
    """
    Finds the first differing character index between two strings.

    Args:
        line1 (str): The first string.
        line2 (str): The second string.

    Returns:
        int: The index of the first character that differs.
             Returns the length of the shorter string if one is a prefix of the other.
             Returns -1 if the strings are identical.
    """
    shorter_len = min(len(line1), len(line2))
    for idx in range(shorter_len):
        if line1[idx] != line2[idx]:
            return idx
    
    if len(line1) != len(line2):
        return shorter_len
        
    return -1

def singleline_diff_format(line1, line2, idx):
    """
    Formats the output for a single-line difference.

    Args:
        line1 (str): The first string.
        line2 (str): The second string.
        idx (int): The index of the first difference.

    Returns:
        str: A formatted string showing the difference, with a trailing newline.
    """
    if idx == -1:
        return ""
    return f"{line1}\n{'=' * idx}^\n{line2}\n"

def multiline_diff(lines1, lines2):
    """
    Finds the first index where the lines in two lists of strings differ.

    Args:
        lines1 (list): The first list of strings.
        lines2 (list): The second list of strings.

    Returns:
        tuple: A tuple (line_idx, char_idx) of the first difference.
               Returns (-1, -1) if the files are identical.
    """
    shorter_len = min(len(lines1), len(lines2))
    for line_idx in range(shorter_len):
        char_idx = singleline_diff(lines1[line_idx], lines2[line_idx])
        if char_idx != -1:
            return (line_idx, char_idx)
            
    if len(lines1) != len(lines2):
        return (shorter_len, 0)

    return (-1, -1)

def file_diff_format(filename1, filename2):
    """
    Compares two files and formats the first difference found.

    Args:
        filename1 (str): The path to the first file.
        filename2 (str): The path to the second file.

    Returns:
        str: A formatted string of the first difference, or "No differences found.\n".
    """
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)
    diff_indices = multiline_diff(lines1, lines2)
    line_idx, char_idx = diff_indices

    if line_idx == -1:
        return "No differences\n"

    # Handle case where one file has more lines than the other
    line1 = lines1[line_idx] if line_idx < len(lines1) else ""
    line2 = lines2[line_idx] if line_idx < len(lines2) else ""

    header = f"Line {line_idx}:\n"
    diff_format = singleline_diff_format(line1, line2, char_idx)
    return header + diff_format
