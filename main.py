def decimal_to_tic_tac_toe(index):
    if index < 0 or index >= 3**9:
        raise ValueError("Index out of range. Must be between 0 and 19682.")
    
    # Convert index to a base-3 (ternary) representation
    ternary = ""
    for _ in range(9):
        ternary = str(index % 3) + ternary
        index //= 3
    
    # Map ternary digits to Tic-Tac-Toe symbols
    board = []
    symbol_map = {'0': ' ', '1': 'X', '2': 'O'}
    for i in range(0, 9, 3):
        row = [symbol_map[ternary[j]] for j in range(i, i + 3)]
        board.append(row)
    
    return board
print(decimal_to_tic_tac_toe(41))
