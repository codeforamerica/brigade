## Attendance & Check In

Attendance is one of the basic metrics that needs to be tracked in movement building. Its useful for tracking the impact of your outreach, the growth of your group over time, and individual participation tracking. Its also incredibly useful for fundraising, considering many grants will accept volunteer hours as their matching funding requirement.

We've built a platform for your Brigade to start tracking attendance.

* https://www.codeforamerica.org/brigade/attendance
* https://www.codeforamerica.org/brigade/Code-for-San-Francisco/attendance

Brigade members can checkin at:

* https://www.codeforamerica.org/brigade/checkin
* https://www.codeforamerica.org/brigade/Code-for-San-Francisco/checkin

We recommend making a short link of the checkin url for your group.

* https://www.codeforamerica.org/brigade/Code-for-San-Francisco/checkin?event=Hack+Night

#### Build your own Brigade attendance tools

Attendance data can be pulled from the Code for America API.

* https://www.codeforamerica.org/api/attendance
* https://www.codeforamerica.org/api/organizations/attendance
* http://www.codeforamerica.org/api/organizations/Code-for-San-Francisco/attendance

Checkins can be posted

* https://www.codeforamerica.org/brigade/checkin
* https://www.codeforamerica.org/brigade/Code-for-San-Francisco/checkin

The schema expected for checkins is:
```
fieldname - type - default - optional - example
name - string - None - Yes - `Margaret Hamilton`
email - string - None - Yes - `apollo@nasa.gov`
event - string - None - Yes - `Moon Landing`
date - datetime - datetime.now() - Yes - `1969-07-20`
cfapi_url - string - None - No - `https://www.codeforamerica.org/api/organizations/Code-for-Houston`
question - string - None - Yes - "What did you do today?"
answer - string - None - Yes - "I invented software engineering and sent the first people to the moon."
```

Testing Checkins

We made a simple testing route to POST to at https://www.codeforamerica.org/brigade/test-checkin/.
It won't save anything, but it will return the correct error codes if you get the `cfapi_url` wrong. It will return your POSTed data back to you if you get succeed with a 200.
