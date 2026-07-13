def translate_coordinates(coordinates):
    """
    Translates chess coordinates (e.g., 'e4') to board indices (row, col).
    
    Args:
        coordinates (str): The chess coordinates in algebraic notation.
        
    Returns:
        tuple: A tuple containing the row and column indices.
    """
    row = int(coordinates[1]) - 1
    col = ord(coordinates[0].lower()) - ord('a')
    return (row, col)

print(translate_coordinates('e2'))# should be (0,0)