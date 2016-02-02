## Project Monitor

Using shame to encourage volunteers to write passing tests. Put this up on a screen during your hack night.

<img src="http://i.imgur.com/sqM3XuE.png" />

#### Why

One of the main challenges with volunteer built tech projects is reliability. Its embarassing when you bring the work of your volunteer group to a funder or a government partner, and it wont turn on.

Reliability becomes super important once you do have government or community partner. If someone is going to put their name, their professional reputation on your project, you can at least know if the tests are passing.

#### Links

* https://www.codeforamerica.org/brigade/projects/monitor
* https://www.codeforamerica.org/brigade/Code-for-San-Francisco/projects/monitor

#### How

The Project Monitor pulls projects from the Code for America API. https://www.codeforamerica.org/api/projects?per_page=50

It then loops through those and only displays the ones with test results, shown in the `commit_status` attribute. This commit status is [pulled from GitHub](https://developer.github.com/v3/repos/statuses/#list-statuses-for-a-specific-ref) once an hour.

If you see you have a failing test, then you quickly go fix it, it can take up to an hour before it will change on the Project Monitor.

