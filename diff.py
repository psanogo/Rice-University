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
        with open(filename, 'r') as file_handle:
            # Read all lines into a list and strip the trailing newline from each.
            lines = [line.rstrip('\n') for line in file_handle.readlines()]
            return lines
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except IOError:
        print(f"Error: Could not read file '{filename}'.")
        return []


def singleline_diff(line1, line2):
    """
    Compares two strings and returns the index of the first difference.

    Args:
        line1 (str): The first string.
        line2 (str): The second string.

    Returns:
        int: The index of the first character where line1 and line2 differ.
             Returns -1 if the lines are identical.
    """
    # Find the length of the shorter line to avoid index errors.
    min_length = min(len(line1), len(line2))

    # Iterate up to the end of the shorter line.
    for idx in range(min_length): # Renamed 'i' to 'idx' for clarity and to satisfy linter
        if line1[idx] != line2[idx]:
            return idx

    # If one line is a prefix of the other, the difference is at the end of the shorter one.
    if len(line1) != len(line2):
        return min_length

    # If we get here, the lines are identical.
    return -1


def singleline_diff_format(line1, line2, idx):
    """
    Formats a string to show the difference between two lines.

    Args:
        line1 (str): The first line.
        line2 (str): The second line.
        idx (int): The index of the first difference.

    Returns:
        str: A formatted string showing both lines and a '^' pointing to the
             difference.
             Example:
             line1
             ===^
             line2
    """
    indicator = '=' * idx + '^'
    return f"{line1}\n{indicator}\n{line2}"


def multiline_diff(lines1, lines2):
    """
    Compares two lists of lines and finds the differences.

    Args:
        lines1 (list): The first list of strings (lines).
        lines2 (list): The second list of strings (lines).

    Returns:
        list: A list of tuples. Each tuple contains the line number (0-indexed)
              and the two differing lines: (line_num, line1, line2).
              This list is empty if the files are identical.
    """
    diffs = []
    num_lines1 = len(lines1)
    num_lines2 = len(lines2)
    max_lines = max(num_lines1, num_lines2)

    for line_num in range(max_lines):
        # Use index bounds to safely get lines or an empty string if out of range
        line1 = lines1[line_num] if line_num < num_lines1 else ""
        line2 = lines2[line_num] if line_num < num_lines2 else ""

        if line1 != line2:
            diffs.append((line_num, line1, line2))
            
    return diffs


def file_diff_format(filename1, filename2):
    """
    Compares two files and returns a formatted string of their differences.

    Args:
        filename1 (str): The path to the first file.
        filename2 (str): The path to the second file.

    Returns:
        str: A formatted string showing all differences, or an empty string
             if the files are identical.
    """
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)

    # If there was an error reading a file, get_file_lines would return [],
    # and multiline_diff will still work correctly.
    
    differences = multiline_diff(lines1, lines2)
    
    if not differences:
        return ""

    formatted_diff_parts = []
    for line_num, line1, line2 in differences:
        # Find the specific character index of the difference.
        diff_index = singleline_diff(line1, line2)
        
        # Format the header for this specific difference.
        header = f"Line {line_num}:\n"
        
        # Get the formatted difference for the two lines.
        formatted_lines = singleline_diff_format(line1, line2, diff_index)
        
        formatted_diff_parts.append(header + formatted_lines)

    # Join all the formatted parts with a newline for separation.
    return "\n".join(formatted_diff_parts)
