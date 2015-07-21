from random import shuffle
from decimal import Decimal
from functools import reduce
from math import floor, sqrt

zero = Decimal(0)
two = Decimal(2)

def get_sqrt_coeff(n, int_dig, man_dig, num_trials):
    """returns an integer x < 2**d such that x * sqrt(n) (mod 1) is close to 1 using a fast randomized algorithm for the subset sum problem"""
    
    two_pow_sq = [Decimal(two**(2 * i) * n).sqrt() % 1 for i in range(-man_dig, int_dig)]
    max_bound = floor(sum(two_pow_sq))
    
    min_dif, min_x = 1, 0
    
    for bound in range(1, max_bound + 1):
        max_sum, exponents = fast_sub_sum(two_pow_sq, bound, num_trials)
        x = rev_bin(exponents, man_dig)
        
        dif = 1 - (Decimal(x**2 * n).sqrt() % 1)
        
        print(x)
        #print(exponents, x, dif, x * dif)
        #print(x * dif)
        
        if dif < min_dif:
            min_dif, min_x = dif, x
            
    return min_x

def rev_bin(exponents, offset):
    
    x = zero
    t = two
    
    for i in exponents:
        x += t**(i - offset)
    
    return x

def fast_sub_sum(num_list, bound, num_trials):
    
    abs_max_sum = 0
    abs_max_soln = list()
    min_x = 0
    
    nl_enum = [[i, num] for i, num in enumerate(num_list)]
    
    for n in range(num_trials):
        ##side effect, but no other code depends on it staying ordered
        shuffle(nl_enum)
        
        cur_max_sum = 0
        cur_max_soln = list()
        
        #first phase (randomized greedy)
        for i_tps in nl_enum:
            i, tps = i_tps
            
            if cur_max_sum + tps <= bound:
                cur_max_sum += tps
                cur_max_soln.append(i_tps)
        
        shuffle(cur_max_soln)
            
        #second phase
        #TODO: introduce simulated-annealing for choice on switch?
        for index in range(len(cur_max_soln)):                    
            max_i, max_tps = cur_max_soln[index]
            rep_i, rep_tps = max_i, max_tps
            
            rem = bound - (cur_max_sum - max_tps)
            
            for i_tps in nl_enum:
                i, tps = i_tps
                
                if i_tps not in cur_max_soln and rep_tps < tps <= rem:
                    dif = tps - rep_tps
                    rem -= dif
                    cur_max_sum += dif
                    
                    rep_i, rep_tps = i_tps
                    cur_max_soln[index] = i_tps
                    
        if cur_max_sum > abs_max_sum:
            abs_max_sum, abs_max_soln = cur_max_sum, cur_max_soln
    
    soln_indices = sorted(map(lambda a: a[0], abs_max_soln))
    
    return [abs_max_sum, soln_indices]
    