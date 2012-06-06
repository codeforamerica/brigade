
class DashboardController < ApplicationController
  def index
    @users = User.count
    @locations = Location.count
    @brigades = Brigade.count
    @applications = Application.count
    @deployed_apps = DeployedApplication.count

  end
end
