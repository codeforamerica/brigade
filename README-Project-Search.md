# Project Search
aka - The Civic Tech App Store

[The Project Search page](http://www.codeforamerica.org/brigade/projects) includes every project from across the civic technology movement. That's [thousands of projects](http://www.codeforamerica.org/brigade/numbers/). The tool includes powerful search and different types of filtering.

By default the projects are returned in order of when they were last worked on.

### How to search
You can search against the project's:
* name
* description
* status
* tags
* programming language
* the organization name that built it - `Code for San Francisco`

You can search by using the search bar or using the [q=bicycles](http://www.codeforamerica.org/brigade/projects?q=bicycles) parameter. You'll see the url of the site update to show your search. This is an exact match of the [cfapi search](http://www.codeforamerica.org/api/projects?q=bicycles).

### Org type
You can filter the Project Search page to only show projects from certain types of organizations. This done by adding the parameter [org_type=Brigade](http://www.codeforamerica.org/brigade/projects?org_type=Brigade). Use the Organization Type buttons to see other examples

### Project Stages
The majority of volunteer built civic tech projects are just experiments. They aren't much use to someone else. Showing a huge list of project with unknown impact isn't our goal. So we came up with Brigade [Project Stages](http://www.codeforamerica.org/brigade/projects/stages) to give some context to the big list of projects. The stages are very much in development and could [use your input](https://github.com/codeforamerica/brigade/milestones/project%20search).

### Civic.json
Project Stages and other metadata are added to projects by including a [civic.json file](https://github.com/codeforamerica/attendance/blob/gh-pages/civic.json) in the top level of the repository.

```
{
    "status": "Experiment", 
    "tags": [
        "inactive", 
        "brigade", 
        "people", 
        "emails"
    ]
}
```

Current attributes accepted are:
* status - which should match one of our project stages to be most useful
* tags - a comma separated list of tags

You can include any other metadata that you'd like, we just wont pull in to the CfAPI. We'll link to the civic.json file though, so you'll have programmatic access that way.