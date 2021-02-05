""" Task 2: Implement generator / iterator which return from NBRB API Currency exchange rate for selected currency
Which uses mp.Process-es

Requirements:
    1. Use NBRB API (https://www.nbrb.by/apihelp/exrates)
    2. Function/Class should implement Iterator Protocol
    3. Must use ``multiprocessing`` module. Do not use concurrent.futures
    4. Input arguments:
        a. ISO Code (3 Letters) or ISO Number (3 Digits) (https://en.wikipedia.org/wiki/ISO_4217). Mandatory
        b. Date from (include). Mandatory
        c. Date To (include). Mandatory
        d. Number of workers. Number of processes. Optional, default = 1
    5. Output iterable value dictionary which contain at least
        Date
        Currency ISO Code
        Currency ISO Number
        Currency English Name
        Currency Exchange Rate
        Currency Scale
    6. !!! Use API which return one record per call !!!
        e.g.: https://www.nbrb.by/api/exrates/rates/298?ondate=2016-7-5

Nice to have:
    Just compare total execution time between multiprocessing, threading implementation
    and sequential (from lesson 5 task 3)
"""
