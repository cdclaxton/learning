def primes(int nb_primes):
    # Define local C variables
    cdef int n, i, len_p
    cdef int[1000] p

    # Restrict the number of primes to protect the stack
    if nb_primes > 1000:
        nb_primes = 1000
    
    # Current number of elements in p
    len_p = 0
    
    n = 2
    while len_p < nb_primes:
        # Is n prime?
        for i in p[:len_p]:
            if n % i == 0:
                break
        else:
            p[len_p] = n
            len_p += 1
        
        n += 1

    return [prime for prime in p[:len_p]]
