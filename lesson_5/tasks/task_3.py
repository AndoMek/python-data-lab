import requests
from datetime import date as _d

""" Task 3: Implement generator / iterator which return from NBRB API Currency exchange rate for selected currency


Requirements:
    1. Use NBRB API (https://www.nbrb.by/apihelp/exrates)
    2. Function/Class should implement Iterator Protocol
    3. Input arguments:
        a. ISO Code (3 Letters) or ISO Number (3 Digits) (https://en.wikipedia.org/wiki/ISO_4217)
        b. Date from (include)
        c. Date To (include)
    4. Output iterable value dictionary which contain at least
        Currency ISO Code
        Currency ISO Number
        Currency English Name
        Currency Exchange Rate
        Currency Scale
"""


class NotFoundError(Exception):
    """NBRB data is blank"""
    pass


def get_exchange_rate(cur_id: str, data_from: str = None, date_to: str = None):
    assert (len(cur_id) == 3)
    if data_from and date_to:
        data = requests.get(
            f"https://www.nbrb.by/API/ExRates/Rates/Dynamics/{int(cur_id)}?startDate={data_from}&endDate={date_to}")
        name = requests.get(f"https://www.nbrb.by/api/exrates/currencies/{cur_id}")
    elif date_to and not date_to:
        data = requests.get(
            f"https://www.nbrb.by/API/ExRates/Rates/Dynamics/{cur_id}?startDate={data_from}&endDate={_d.today().strftime('%Y-%m-%d')}")
        name = requests.get(f"https://www.nbrb.by/api/exrates/currencies/{cur_id}")
    else:
        data = requests.get(
            f"https://www.nbrb.by/API/ExRates/Rates/Dynamics/{cur_id}?startDate={_d.today().strftime('%Y-%m-%d')}&endDate={_d.today().strftime('%Y-%m-%d')}")
        name = requests.get(f"https://www.nbrb.by/api/exrates/currencies/{cur_id}")
    if not data.json():
        raise NotFoundError("Can not find Exchange Rate")

    if data.status_code != 200:
        raise requests.HTTPError(f"Can not get data from https://www.nbrb.by/api/exrates/currencies/{cur_id}")
    name, data = name.json(), data.json()
    for time in data:
        yield dict(zip(("Cur_ISO_Code", "Cur_ISO_Name", "Cur_Eng_Name", "Cur_Exchange_Rate", "Cur_Scale"),
                       (name['Cur_ID'], name['Cur_Abbreviation'], name['Cur_Name_Eng'], name['Cur_Scale'],
                        time['Cur_OfficialRate'])))


if __name__ == "__main__":
    cur = get_exchange_rate('298', '2020-10-11', '2020-12-12')
    for day in cur:
        print(day)
