import dateutil.parser
import flask
from jinja2 import evalcontextfilter, Markup, escape


from datetime import datetime
import re


PARAGRAPH_RE = re.compile(r'(?:\r\n|\r|\n){2,}')


filters = flask.Blueprint('filters', __name__)


@filters.app_template_filter("join_list")
def join_list(value):
    values = list(value)
    if len(values) == 0:
        return ""
    elif len(values) == 1:
        return values[1]
    elif len(values) == 2:
        return "{0} and {1}".format(values[0], values[1])
    elif len(values) > 2:
        return ", ".join(values[0:-1]) + ', and ' + values[-1]


@filters.app_template_filter("brigade_description")
def brigade_description(brigade):
    if "Official" in brigade['type'] and "Brigade" in brigade['type']:
        return "{0} is a group of volunteers in {1} working on projects with government and " \
               "community partners to improve peoples' lives.".format(
                    brigade['name'], brigade['city'])
    else:
        return "{0} is a group of civic technologists working to build a better " \
            "government. They're based in {1}.".format(
                    brigade['name'], brigade['city'])


@filters.app_template_filter("split_hyphen")
def split_hyphen(string):
    ''' Replaces hyphens in the passed string with spaces
    '''
    return string.replace("-", " ")


# see: http://flask.pocoo.org/snippets/33/
# and: http://stackoverflow.com/questions/12288454/how-to-import-custom-jinja2-filters-from-another-file-and-using-flask # noqa
@filters.app_template_filter("timesince")
def friendly_time(dt, past_="ago", future_="from now", default="Just now"):
    ''' Returns string representing "time since" or "time until" e.g. 3 days ago, 5 hours from now etc.
    '''

    now = datetime.utcnow()
    try:
        # 2015-02-26 03:45:21
        trimmed_time = dt[:19]
        dt = datetime.strptime(trimmed_time, "%Y-%m-%d %H:%M:%S")
    except Exception:
        pass

    try:
        # Thu, 26 Feb 2015 03:45:21 GMT
        dt = datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S %Z")
    except Exception:
        pass

    if type(dt) != datetime:
        return default

    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s %s" % (
                period,
                singular if period == 1 else plural,
                past_ if dt_is_past else future_
            )

    return default


@filters.app_template_filter("format_time")
def format_time(datetime_str):
    return dateutil.parser.parse(datetime_str).strftime("%A, %b %d, %Y @ %-I:%M %p")


# copied from: http://flask.pocoo.org/snippets/28/ (in public domain)
@filters.app_template_filter("nl2br")
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in PARAGRAPH_RE.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
