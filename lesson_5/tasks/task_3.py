from datetime import timedelta, datetime, date as _d
import requests
""" Task 1: Implement generator / iterator which return from NBRB API Currency exchange rate for selected currency
Which uses threading.Threads

Requirements:
    1. Use NBRB API (https://www.nbrb.by/apihelp/exrates)
    2. Function/Class should implement Iterator Protocol
    3. Must use ``threading`` module. Do not use concurrent.futures
    4. Input arguments:
        a. ISO Code (3 Letters) or ISO Number (3 Digits) (https://en.wikipedia.org/wiki/ISO_4217)
        b. Date from (include). Mandatory
        c. Date To (include). Mandatory
        d. Number of workers. Number of threads. Optional, default = 1
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
    Just compare total execution time between threading implementation and sequential (from lesson 5 task 3)
"""


class NotFoundError(Exception):
    """NBRB data is blank"""
    pass



# Variable for save English name
eng_name = ''



def get_exchange_rate_by_day(urls, s):
    """Get exchange rate by day

    Args:
        urls: Url Queue
        s: requests.Session

    Returns:
        dict
    """
    data = s.get(urls, verify=False)
    if not data.json():
        raise NotFoundError("Can not find Exchange Rate")
    data.raise_for_status()
    data = data.json()
    return (
        dict(zip(("Date", "Cur_ISO_Code", "Cur_ISO_Name", "Cur_Eng_Name", "Cur_Exchange_Rate", "Cur_Scale"),
                 (data['Date'], data['Cur_ID'], data['Cur_Abbreviation'], eng_name, data['Cur_Scale'],
                  data['Cur_OfficialRate']))))


def get_eng_name(cur_id: str):
    """Get English Name

    Args:
        cur_id:  Currency ISO Number

    Returns:
        English name
    """
    assert (len(cur_id) == 3)
    name = requests.get(f"https://www.nbrb.by/api/exrates/currencies/{int(cur_id)}", verify=False)
    name.raise_for_status()
    return name.json()['Cur_Name_Eng']


def get_exchange_rate(cur_id: str,
                      date_from: str = _d.today().strftime('%Y-%m-%d'),
                      date_to: str = _d.today().strftime('%Y-%m-%d')):
    """ NBRB  Currency exchange rate for selected currency

    Args:
        cur_id: ISO Code (3 Letters). str
        date_from: Date from. default today
        date_to: Date to. default today
        workers: Number of threads. Optional, default = 1

    Returns:
        generator / iterator exchange rate [day_from; date_to]
    """
    global len_queue
    end, start = datetime.strptime(date_to, '%Y-%m-%d'), datetime.strptime(date_from, '%Y-%m-%d')
    for n in range(int((end - start).days) + 1):
        with requests.Session() as s:
            yield get_exchange_rate_by_day(f"https://www.nbrb.by/api/exrates/rates/{int(cur_id)}?ondate={(start + timedelta(n)).strftime('%Y-%m-%d')}", s)


if __name__ == "__main__":
    import warnings
    import time
    ar = []
    for i in range(100):
        start = time.time()
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        eng_name = get_eng_name('298')
        cur = get_exchange_rate('298', '2020-10-11', '2020-10-25')
        for dict_ in cur:
            print(dict_)
        ar.append(time.time() - start)
    print(sum(ar)/len(ar))

