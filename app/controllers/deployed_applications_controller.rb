class DeployedApplicationsController < ApplicationController

  def show
    @deployed_application = DeployedApplication.find(params[:id])
  end

  def index
    @filter_type = params[:filter_by]
    @deployed_applications = DeployedApplication.all
  end
end
