from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from django.urls import reverse

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = Event.objects.by_day(day)

        if day != 0:
            date_str = str(self.year) + '-' + str(self.month).zfill(2) + \
                '-' + str(day).zfill(2)
            date = datetime.strptime(date_str, '%Y-%m-%d')
            cell_style = ''
            url = ''

            if events_per_day.count() > 0:
                # Day with events
                cell_style = 'btn-warning'
                if date.day == datetime.today().day:
                    cell_style += 'font-weight-bold'
                url = events_per_day[0].get_html_url
            else:
                # Day without events
                cell_style = 'btn-outline-secondary'
                if date.date() == datetime.today().date():
                    cell_style = 'font-weight-bold text-dark'
                url_str = reverse('create_event_on_date', args=(date.strftime('%Y-%m-%d'),))
                url = f'href="{url_str}"'

            return f"<td class=''><a class='date {cell_style}' \
                    {url}>{day}</a></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(date__year=self.year, date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

