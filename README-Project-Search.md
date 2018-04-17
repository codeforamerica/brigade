# A guide to Project Search and the civic.json

## Project Search
The [Project Search](http://www.codeforamerica.org/brigade/projects) page is a new service we built to search across thousands of civic technology projects. Go try it out, we think it's pretty useful.

#### How to search
You can search by using the search bar or using the `q` parameter like so: [q=bicycles](http://www.codeforamerica.org/brigade/projects?q=bicycles). When you submit a query, you'll see the url of the site update to show your search. This is an exact match to the [cfapi search](http://www.codeforamerica.org/api/projects?q=bicycles).

Your search will match against the project's `name`, `description`, `tags`, `languages`, and `organization_name`.

In addition, you can filter by the `type` of a project's organization. Search for organization type by adding the `organization_type` parameter like so: [organization_type=Brigade](http://www.codeforamerica.org/brigade/projects?organization_type=Brigade). The options are `Brigade`, `Code for All`, `Government`. Code for America's projects are included under Code for All.

By default, projects are listed in order of most recently updated. When searching, results are listed in order of most relevant.
