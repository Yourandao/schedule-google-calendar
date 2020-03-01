from datetime import datetime, timedelta

class DateProvider:
    @staticmethod
    def getDateFromWeek(year, week, day):
        week += 6
        daydate = datetime.strptime(f'{year}-W{week - 1}-1', '%Y-W%W-%w').date() + timedelta(days=day)

        return daydate
