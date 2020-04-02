import datetime


class Today(object):
    today = datetime.datetime.today()
    week = today.isocalendar()[1]
    month = today.month
    year = today.year

    def __init__(self):
        self.day = self.today
        self.week = self.week
        self.month = self.month
        self.year = self.year

    def get_yesterday(self):
        yesterday = self.today - datetime.timedelta(days=1)
        day = yesterday.day
        week = yesterday.isocalendar()[1]
        month = yesterday.month
        year = yesterday.year
        yesterdaysDate = {"day": day, "week": week,
                          "month": month, "year": year}
        return yesterdaysDate

    def is_new_month(self):
        yesterday = self.get_yesterday()
        if self.month > yesterday['month']:
            return True
        elif self.month == 1 and yesterday['month'] == 12:
            return True
        else:
            return False
