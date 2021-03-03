from csv import reader
import pandas_datareader as web


def Initial_Parameters(Company):
        # Read csv file into a list of lists
    with open(Company + '.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_lists = list(csv_reader)

    DATE = []
    OPEN = []
    HIGH = []
    LOW = []
    CLOSE = []
    ADJ_CLOSE = []
    VOLUME = []

    for i in list_of_lists:
        DATE.append(i[0])
        OPEN.append(i[1])
        HIGH.append(i[2])
        LOW.append(i[3])
        CLOSE.append(i[4])
        ADJ_CLOSE.append(i[5])
        VOLUME.append(i[6])

    # Remove column label 
    DATE = DATE[1:len(OPEN)]
    OPEN = OPEN[1:len(OPEN)]
    HIGH = HIGH[1:len(OPEN)]
    LOW = LOW[1:len(OPEN)]
    CLOSE = CLOSE[1:len(OPEN)]
    ADJ_CLOSE = ADJ_CLOSE[1:len(OPEN)]
    VOLUME = VOLUME[1:len(OPEN)]

    Initial = [DATE, OPEN, HIGH, LOW, CLOSE, ADJ_CLOSE, VOLUME]
    return Initial