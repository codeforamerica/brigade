class Locations::DeployedApplicationsController < ApplicationsController

  def index
    @location = Location.find(params[:location_id])

    @deployed_applications = @location.deployed_applications.search(params[:query])
  end
end
