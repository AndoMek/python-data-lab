from datetime import timedelta, datetime, date as _d
import threading
import requests
from queue import Queue, Empty

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


def get_exchange_rate_by_day(urls, eng_name, s):
    """Get exchange rate by day

    Args:
        urls: Url Queue
        eng_name: Currency English Name
        s: requests.Session

    Returns:
        dict.
            Date
            Currency ISO Code
            Currency ISO Number
            Currency English Name
            Currency Exchange Rate
            Currency Scale
    """

    data = s.get(urls, verify=False)
    if not data.json():
        raise NotFoundError("Can not find Exchange Rate")
    data.raise_for_status()
    data = data.json()
    return (
        {
            "Date": data['Date'],
            "Cur_ISO_Code": data['Cur_ID'],
            "Cur_ISO_Name": data['Cur_Abbreviation'],
            "Cur_Eng_Name": eng_name,
            "Cur_Scale": data['Cur_Scale'],
            "Cur_Exchange_Rate": data['Cur_OfficialRate'],
        })


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


def thread_function(args_queue, output_queue, input_event, output_event):
    """

    Args:
        args_queue: Arguments queue. Urls, english name, request.Session
        output_queue: dictionary queue. see "get_exchange_rate_by_day"
        input_event: args events
        output_event: worker events

    Returns:

    """
    while True:
        try:
            args = args_queue.get(timeout=0.1)
        except Empty:
            if input_event.is_set():
                break
            continue
        result = get_exchange_rate_by_day(*args)
        output_queue.put(result)

    output_event.set()


def url_with_date(end, start_, cur_id):
    for n in range(int((end - start_).days) + 1):
        yield f"https://www.nbrb.by/api/exrates/rates/{int(cur_id)}?ondate={(start_ + timedelta(n)).strftime('%Y-%m-%d')}"


def get_exchange_rate(cur_id: str,
                      date_from: str = _d.today().strftime('%Y-%m-%d'),
                      date_to: str = _d.today().strftime('%Y-%m-%d'), workers: int = 1):
    """ NBRB  Currency exchange rate for selected currency

    Args:
        cur_id: ISO Code (3 Letters). str
        date_from: Date from. default today
        date_to: Date to. default today
        workers: Number of threads. Optional, default = 1

    Returns:
        generator / iterator exchange rate [day_from; date_to]
    """
    urls, output_dict = Queue(), Queue()
    args_event = threading.Event()
    threads, events = [], []
    eng_name = get_eng_name(cur_id)
    end, start_ = datetime.strptime(date_to, '%Y-%m-%d'), datetime.strptime(date_from, '%Y-%m-%d')
    with requests.Session() as s:
        for _ in range(workers):
            event = threading.Event()
            td = threading.Thread(target=thread_function, args=(urls, output_dict, args_event, event))
            td.start()
            threads.append(td)
            events.append(event)

        for url in url_with_date(end, start_, cur_id):
            urls.put([url, eng_name, s])

        args_event.set()
        while True:
            try:
                result = output_dict.get(timeout=0.1)
            except Empty:
                if all(e.is_set() for e in events):
                    break
                continue

            yield result


if __name__ == "__main__":
    import warnings
    import time

    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    ar = []
    for i in range(10):
        start = time.time()
        cur = get_exchange_rate('298', '2020-10-11', '2020-10-25', 3)
        for dict_ in cur:
            print(dict_)
        print(time.time() - start)
        ar.append(time.time() - start)
    print(sum(ar) / len(ar))
