import re
import hashlib

def compute_sha256(s: str) -> str:
    """
    Compute SHA-256 hash of a string.
    
    Args:
        s: String to be hashed
        
    Returns:
        Hexadecimal representation of the SHA-256 hash
        
    Raises:
        ValueError: If input_string is None or not a string
    """
    if s is None or not isinstance(s, str):
        raise ValueError("Input must be a non-null string")

    normalized_string = s.encode('utf-8')
    hash_object = hashlib.sha256(normalized_string)
    
    return hash_object.hexdigest()


def is_palindrome(s: str) -> bool:
    s = s.lower()
    i, j, is_pali = 0, len(s) - 1, True
    while i < j:
        if s[i] != s[j]:
            is_pali = False
            break
        i += 1
        j -= 1
    return is_pali

def count_unique_characters(s: str) -> int:
    """
    Counts the number of unique characters in a given string.

    Args:
        s: The input string.

    Returns:
        The number of unique characters in the string.
    """
    if s is None:
        return 0
    return len(set(s))

def compute_word_count(s: str) -> int:
    """
    Counts the number of words in a sentence.

    Args:                                                          s: The input string.

    Returns:
        The number of words in a sentence.
    """
    if s is None:
        return 0
    return len(re.findall(r'\b\w+\b', s))

def character_frequency_map(s: str) -> dict:
    if s is None:
        return {}
    return {c: s.count(c) for c in s}

