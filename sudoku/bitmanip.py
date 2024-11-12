def set_bit_to_one_at(bitmask=int, pos=int):
    return bitmask | (1 << pos)
    
def set_bit_to_zero_at(bitmask=int, pos=int):
    return bitmask & (~(1 << pos))

def get_bit_length(x=int):
    i = 0
    while x >= 1:
        x //= 2
        i += 1
    return i

def get_bit_count(x=int):
    i = 0
    while x >= 1:
        i += x & 1
        x >>= 1
    return i