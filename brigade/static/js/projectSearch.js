
var Projects = React.createClass({
  getInitialState: function(){
    return {
      projects : {{projects | safe}}
    }
  },
  render: function() {
    return (
      <p>
      {this.state.projects.map(function(project){
        return <Project project={project} />;
      })}
      </p>
    )
  }
});

var Project = React.createClass({
  render: function() {
    return(
      <li className="project card">

        <div className="card-head">
        </div>

        <div className="card-body">

          <h3>{this.props.project.name}</h3>
          <p>{this.props.project.description}</p>

          <a href="{this.props.project.link_url}" className="button-bold">View the project</a>
          <a href="{this.props.project.code_url}" className="button-bold">Contribute on Github</a>

        </div>
      </li>
    );
  }
});

// Do the thing
ReactDOM.render(
  <Projects source="https://cfapi-staging.herokuapp.com/api/projects" />,
  document.getElementById('projects')
);