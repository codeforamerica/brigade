class DeployedApplicationsController < ApplicationController

  def show
    @deployed_application = DeployedApplication.find(params[:id])
    @app = AppDecorator.new(@deployed_application.application)
  end

  def index
    @filter_type = params[:filter_by]
    @deployed_applications = DeployedApplication.all
  end
end
