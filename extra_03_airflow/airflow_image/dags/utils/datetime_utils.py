# This converts get from Frostbolt Common Producer Framework

from datetime import date, datetime, timedelta, timezone


def _format_time(hh, mm, ss, us, timespec='auto'):
    """Backport Python 3.7 function datetime._format_time from datetime module
       Use for config_type time in ISO 8601 config_type
    """

    specs = {
        'hours': '{:02d}',
        'minutes': '{:02d}:{:02d}',
        'seconds': '{:02d}:{:02d}:{:02d}',
        'milliseconds': '{:02d}:{:02d}:{:02d}.{:03d}',
        'microseconds': '{:02d}:{:02d}:{:02d}.{:06d}'
    }

    if timespec == 'auto':
        # Skip trailing microseconds when us==0.
        timespec = 'microseconds' if us else 'seconds'
    elif timespec == 'milliseconds':
        us //= 1000
    try:
        fmt = specs[timespec]
    except KeyError:
        raise ValueError('Unknown timespec value')
    else:
        return fmt.format(hh, mm, ss, us)


def _format_offset(off):
    """Backport Python 3.7 function from datetime module
       Use for config_type timezone offset in ISO 8601 config_type
       Minor changes: instead of 00:00 offset use 'Z'
    """
    s = ''
    if off is not None:

        if off.days < 0:
            sign = "-"
            off = -off
        else:
            sign = "+"
        hh, mm = divmod(off, timedelta(hours=1))
        mm, ss = divmod(mm, timedelta(minutes=1))

        # Custom condition for check zero offset
        if hh == 0 and mm == 0:
            if not ss or \
                    (ss and ss.seconds == 0 and (not ss.microseconds or (ss.microseconds and ss.microseconds == 0))):
                return "Z"

        s += "%s%02d:%02d" % (sign, hh, mm)
        if ss or ss.microseconds:
            s += ":%02d" % ss.seconds

            if ss.microseconds:
                s += '.%06d' % ss.microseconds
    return s


def datetime_isoformat(dt: datetime, sep='T', timespec='auto'):
    """Backport Python 3.7 function datetime.datetime.isoformat()
       Use for config_type datetime to ISO 8601 config_type
    """
    s = ("%04d-%02d-%02d%c" % (dt.year, dt.month, dt.day, sep) +
         _format_time(dt.hour, dt.minute, dt.second,
                      dt.microsecond, timespec))

    off = dt.utcoffset()
    tz = _format_offset(off)
    if tz:
        s += tz

    return s


def date_isoformat(dt: date):
    """Backport Python 3.7 function datetime.date.isoformat()
       Use for config_type date to ISO 8601 config_type
    """
    return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


def utc_now():
    return datetime.now(tz=timezone.utc)
