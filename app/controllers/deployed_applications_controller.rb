class DeployedApplicationsController < ApplicationController

  def show
    @deployed_application = DeployedApplication.find(params[:id])
    @app = AppDecorator.new(@deployed_application.application)
  end

  def index
    @filter_type = params[:filter_by]
    @deployed_applications = DeployedApplication.all
  end

  def edit
    @deployed_application = DeployedApplication.find(params[:id])
  end

  def update
    @deployed_application = DeployedApplication.find(params[:id])

    if @deployed_application.update_attributes(params[:deployed_application])
      redirect_to deployed_application_path(@deployed_application)
    else
      render :edit
    end
  end
end
