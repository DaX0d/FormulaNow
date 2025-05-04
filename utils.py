def msk(t: str) -> str:
    '''Принимает время по гринвичу, возвращает по московскому времени'''
    h = (int(t[:2].lstrip('0') or '0') + 3) % 24
    return '{:02d}{}'.format(h, t[2:])


def prev_date(day, month, d) -> tuple[int, int]:
    '''Принимает дату (день и месяц), возвращает дату, отмотанную назад на указанное кол-во дней в виде кортежа'''

    if day - d > 0:
        return (day - d, month)
    
    new_month = month - 1

    if new_month - 1 < 8:
        match new_month % 2:
            case 0:
                return (day - d + 30, new_month)
            case 1:
                return (day - d + 31, new_month)
    else:
        match new_month % 2:
            case 0:
                return (day - d + 31, new_month)
            case 2:
                return (day - d + 30, new_month)
