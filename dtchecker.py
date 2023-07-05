def main():
    from datetime import datetime as dt

    dttoday = str(dt.today())
    dtsplit = dttoday.split(" ")
    date = dtsplit[0]
    time = dtsplit[1]
    day = dt.today().weekday()
    timesplit = time.split(":")
    hour = int(timesplit[0])
    minute = int(timesplit[1])
    if minute > 30:
        hour += 0.5
    date = str(date).replace("-", "")
    date = str(date)
    print(hour)
    if (hour >= 7) and (hour < 22.5):
        return(1, date)
    else:
        return(0, date)

if __name__ == '__main__':
    main()
