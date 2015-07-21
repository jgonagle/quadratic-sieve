import math
import decimal as dec

def get_gcf_conv(int_part, part_num_denom, repeats):
    """generates the successive convergents of the generalized convergent fraction with integer part int_part and pairs of partial numerators and denominators part_num_denom
    
    int_part must be an integer
    part_num_denom is a list/iterator/generator of pairs of partial numerators and denominators.  part_num_denom can only be a generator or iterator in the event that repeats is false
    repeats is a boolean specifying whether the list of partial numerators and denominators is cyclic in the case that part_num_denom is not an iterator or generator"""
    
    #continuant numerator and denominator for current convergent
    a_n = int_part
    b_n = 1
    
    #continuant numerator and denominator for one convergent before
    a_nm1 = 1
    b_nm1 = 0
    
    yield [a_n, b_n]
    
    if repeats:
        #length of cycle of partial numerators and denominators
        pnd_rep_len = len(part_num_denom)
        
        i = 0
        
        while True:
            p_num, p_denom = part_num_denom[i]
            
            a_n, b_n, a_nm1, b_nm1 = get_gcf_recur(p_num, p_denom, a_n, b_n, a_nm1, b_nm1)
            yield [a_n, b_n]
            
            i = (i + 1) % pnd_rep_len          
    else:
        for p_num, p_denom in part_num_denom:
            a_n, b_n, a_nm1, b_nm1 = get_gcf_recur(p_num, p_denom, a_n, b_n, a_nm1, b_nm1)
            yield [a_n, b_n]
        
  
def get_gcf_recur(p_num, p_denom, a_nm1, b_nm1, a_nm2, b_nm2):

    temp_a_nm1, temp_b_nm1 = a_nm1, b_nm1
    
    a_n = p_denom * a_nm1 + p_num * a_nm2
    b_n = p_denom * b_nm1 + p_num * b_nm2
    
    return [a_n , b_n, temp_a_nm1, temp_b_nm1]

def get_sqrt_gcfc(n, x):
    
    y = n - x**2
    
    return get_gcf_conv(x, [[y, 2 * x]], True)

def print_sqrt_conv(n, x, num_prints):
    
    sqrt_gen = get_sqrt_gcfc(n, x)
    sqrt_n = dec.Decimal(n).sqrt()
    
    for i, pnd in enumerate(sqrt_gen):
        if i < num_prints:
            a_n, b_n = pnd
            approx = dec.Decimal(a_n) / dec.Decimal(b_n)
            error = sqrt_n - approx
            
            print("Convergent {!s}: {!s} / {!s} = {!s}, Error: {!s}".format(i, a_n, b_n, approx, error))
        else:
            break        