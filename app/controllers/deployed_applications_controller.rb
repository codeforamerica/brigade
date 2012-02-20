class DeployedApplicationsController < ApplicationController

  def index
    @filter_type = params[:filter_by]
    @deployed_applications = DeployedApplication.all
  end
end
