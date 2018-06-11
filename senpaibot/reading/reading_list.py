from datetime import datetime
from senpaibot.orderedset import OrderedSet

reading_list = [
    ('Capítulo 1', datetime(2018, 5, 22)),
    ('Capítulo 2', datetime(2018, 6, 10)),
    ('Capítulo 3', datetime(2018, 6, 11)),
    ('Capítulo 4', datetime(2018, 6, 12)),
    ('Capítulo 5', datetime(2018, 7, 10)),
    ('Capítulo 6', datetime(2018, 7, 11)),
    ('Capítulo 7', datetime(2018, 7, 12)),
]

undated_reading_set = OrderedSet([read[0] for read in reading_list])
