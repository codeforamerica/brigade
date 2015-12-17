# A guide about Project Search and civic.json


## Project Search
The [Project Search](http://www.codeforamerica.org/brigade/projects) page is a new service we built to search across [thousands](http://www.codeforamerica.org/brigade/numbers/) of civic technology projects. Go try it out, we think its pretty useful.

#### How to search
You can search by using the search bar or using the [q=bicycles](http://www.codeforamerica.org/brigade/projects?q=bicycles) parameter. You'll see the url of the site update to show your search. This is an exact match of the [cfapi search](http://www.codeforamerica.org/api/projects?q=bicycles).

Your search will try and match against the project's `name`, `description`, `status`, `tags`, `languages`, and `organization_name` such as "Code for San Francisco".

You can also filter types of organizations. This done by adding the parameter [organization_type=Brigade](http://www.codeforamerica.org/brigade/projects?organization_type=Brigade). The options are `Brigade`, `Code for All`, `Government`. Code for America's projects are included under Code for All.

By default, the returns projects in order of most recently updated. When searching, it returns in order of most relevant.

#### Stages
You’ll notice that many projects have a Project Stage. These stages are [explained in detail](http://www.codeforamerica.org/brigade/projects/stages) and are meant to give some context to this big pile of projects. If you are government employee looking for [a tool to help find preschools](http://www.codeforamerica.org/brigade/projects?q=official,%20preschool), you’ll probably only want to see finished `Official` projects. If you are a Brigade leader looking for [transit data projects](http://www.codeforamerica.org/brigade/projects?q=Experiment,%20transit%20data) for your volunteers to hack on, you’ll want to find `Alpha` and `Experiment` projects that still need contributors. Get it?

#### Tags
The Project Search searches from a bunch of attributes about the project, yet sometimes the right term just isn’t in there. Thats where tags come in. Tags are a great catchall place to put metadata about the project. `transit, buses, open data, iOS, California` are examples of the random things people might want to search for and find for a specific project. We’ll keep watching what tags are being used and what people are searching for to produce a recommended list.

## Civic.json
To add this metadata about stages and tags to the project, we’re including a civic.json file in each project. The idea of a civic.json comes from [Beta.NYC](https://github.com/BetaNYC/civic.json) and [Chi Hack Night](https://github.com/open-city/civic-json-worker). In the Code for America version of the idea, we’re only including two attributes, `status` and `tags`. You can include other data in there, yet you won’t find it on the Project Search page yet.

Include the civic.json file at the top level of your project.

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
To add these important stages and tags to your project, you can use the form we built into the project search page. If your project doesn’t have civic.json file yet, you’ll see a button to add one.

![add a civic.json file](http://i.imgur.com/lhQ7GIL.png)

The url for the form follows the pattern of `http://www.codeforamerica.org/brigade/<Brigade-Name>/projects/<project-name>/add-civic-json`. An [example](http://www.codeforamerica.org/brigade/Code-for-America/projects/brigade/add-civic-json).

You'll need to log into Github. Once you fill out the form, it will send a Pull Request from your Github account to the project for their approval or rejection.

If you are having trouble, you can always build your own civic.json and add it to the top level of the project.

## Advice for Brigades
We recommend that your Delivery Lead or Captain take time to once a month to review each of your group’s projects and update the metadata about it. 

#### Why?
The Project Search page is already really popular and is becoming the main way other Brigades find out about your group’s work. Its important to keep your Brigade's projects info up to date because:
* Project Search is how civic hackers across the country will find projects to contribute to.
* Project Search is how city employees will find projects to solve problems in their cities.
* Code for America will give different types of support to different project stages.
* Your Brigade could offer different types of support to different project stages.

#### How
1. Go to your Brigade's list of projects. You can just search for your group like [http://www.codeforamerica.org/brigade/projects?q=Code+for+San+Francisco](http://www.codeforamerica.org/brigade/projects?q=Code+for+San+Francisco) or go to your Brigade's individual project page like [https://www.codeforamerica.org/brigade/Code-for-San-Francisco/projects](https://www.codeforamerica.org/brigade/Code-for-San-Francisco/projects).
2. Review each project. Talk to the project team, check out their live examples, their README.
3. Choose the appropriate [project stage](http://www.codeforamerica.org/brigade/projects/stages). 
4. Choose the appropriate tags. Our initial list of what looks useful is search terms, city name, and tech stack.
5. Make the civic.json file. You can [use our form](#adding-a-civicjson-to-your-project) or edit the civic.json file direct on Github.
