class Brigades::DeployedApplicationsController < ApplicationsController

  def index
    @brigade = Brigade.find(params[:brigade_id])

    @deployed_applications = @brigade.deployed_applications.search(params[:query])
  end
end
