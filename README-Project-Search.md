# A guide to Project Search and the civic.json

## Project Search
The [Project Search](http://www.codeforamerica.org/brigade/projects) page is a new service we built to search across [thousands](http://www.codeforamerica.org/brigade/numbers/) of civic technology projects. Go try it out, we think it's pretty useful.

#### How to search
You can search by using the search bar or using the `q` parameter like so: [q=bicycles](http://www.codeforamerica.org/brigade/projects?q=bicycles). When you submit a query, you'll see the url of the site update to show your search. This is an exact match to the [cfapi search](http://www.cfapi-staging.herokuapp.com/api/projects?q=bicycles).

Your search will match against the project's `name`, `description`, `tags`, `languages`, and `organization_name`.

In addition, you can filter by project `status`, [explained below](#stages), and by the `type` of a project's organization. Search for organization type by adding the `organization_type` parameter like so: [organization_type=Brigade](http://www.codeforamerica.org/brigade/projects?organization_type=Brigade). The options are `Brigade`, `Code for All`, `Government`. Code for America's projects are included under Code for All.

By default, projects are listed in order of most recently updated. When searching, results are listed in order of most relevant.

#### Stages
You'll notice that many projects have a Project Stage. These stages are [explained in detail here](http://www.codeforamerica.org/brigade/projects/stages), and are meant to give some context to how complete a project is. If you are government employee looking for [a tool to help find preschools](http://www.codeforamerica.org/brigade/projects?status=Official&q=preschool), you'll probably only want to see finished, `status=Official`, projects. If you are a Brigade leader looking for [transit data projects](http://www.codeforamerica.org/brigade/projects?status=Experimentq=transit%20data) for your volunteers to hack on, you'll want to find `status=Alpha` and `status=Experiment` projects that still need contributors. Get it?

We call them project stages but in the civic.json they are called status. Sorry if it's confusing. The valid statuses that we are using are `Experiment`, `Alpha`, `Beta`, and `Official`.

#### Tags
The Project Search queries a bunch of attributes about a project, but sometimes the right term just isn't in there. That's where tags come in. Tags are a great catchall place to put metadata about a project. `transit, buses, open data, iOS, California` are examples of the random things people might want to search for and find for a specific project. We'll keep watching what tags are being used and what people are searching for to produce a recommended list.

## Civic.json
To add this metadata about stages and tags to the project, we recommend including a `civic.json` file in each project's repo. The civic.json concept comes from [Beta.NYC](https://github.com/BetaNYC/civic.json) and [Chi Hack Night](https://github.com/open-city/civic-json-worker). In the Code for America implementation of the idea, we're only expecting to find two attributes: `status` and `tags`. You can include other data in the file, but you won't see it displayed on the Project Search page.

Include the civic.json file at the top level of your project's repo.

#### Example
```
{
    "status": "Experiment", 
    "tags": [
        "San Francisco",
        "California",
        "affordable housing", 
        "iOS", 
        "CodeAcross 2014"
    ]
}
```

#### Adding a civic.json to your project
To add these important stages and tags to your project, you can use the form that we've built into the project search page. If your project doesn't have a civic.json file yet, you'll see a button like this:

![add a civic.json file](http://i.imgur.com/lhQ7GIL.png)

The url for the form follows the pattern of `http://www.codeforamerica.org/brigade/<Brigade-Name>/projects/<project-name>/add-civic-json`. For example: [http://www.codeforamerica.org/brigade/Code-for-America/projects/brigade/add-civic-json](http://www.codeforamerica.org/brigade/Code-for-America/projects/brigade/add-civic-json).

You'll need to log into Github. When you fill out and submit the form, it will send a Pull Request from your Github account to the project for their approval or rejection.

If you are having trouble with the form, you can always create your own civic.json file and add it to the top level of the project repo.

## Advice for Brigades
We recommend that your Delivery Lead or Captain take time to once a month to review each of your group's projects and update the metadata about it.

#### Why?
The Project Search page is already really popular and is becoming the main way other Brigades find out about your group's work. It's important to keep your Brigade's project info up to date because:
* Project Search is how civic hackers across the country will find projects to contribute to.
* Project Search is how city employees will find projects to solve problems in their cities.
* Code for America will give different types of support to different project stages.
* Your Brigade could offer different types of support to different project stages.

#### How
1. Go to your Brigade's list of projects. You can just search for your group like [http://www.codeforamerica.org/brigade/projects?q=Code+for+San+Francisco](http://www.codeforamerica.org/brigade/projects?q=Code+for+San+Francisco) or go to your Brigade's individual project page like [https://www.codeforamerica.org/brigade/Code-for-San-Francisco/projects](https://www.codeforamerica.org/brigade/Code-for-San-Francisco/projects).
2. Review each project. Talk to the project team, check out their live examples, their README.
3. Choose the appropriate [project stage](http://www.codeforamerica.org/brigade/projects/stages). 
4. Choose appropriate tags: Your city name, tech stack details; any term that someone might use to search for or categorize your project.
5. Make the civic.json file. You can [use our form](#adding-a-civicjson-to-your-project) or create and edit a civic.json file directly on Github.
