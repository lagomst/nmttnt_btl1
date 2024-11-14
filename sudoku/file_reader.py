def read_from_file(filename):
    """
    Read from file, return grid size as int and the board's values as an array
    """
    file = open(filename, "r")
    grid_size = int(file.readline())
    
    array = []
    
    lines = file.readlines()
    for line in lines:
        list_int = list(map(int,  line.split(' ')))
        array.extend(list_int)
    
    return grid_size, array