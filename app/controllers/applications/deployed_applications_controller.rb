class Applications::DeployedApplicationsController < DeployedApplicationsController
  load_resource :application

  def new
    @deployed_application = @application.deployed_applications.build
    @location = @deployed_application.build_location
    @brigade = @deployed_application.build_brigade

    authorize! :create, @deployed_application
  end

  def create
    @deployed_application = @application.deployed_applications.build params[:deployed_application]

    if @deployed_application.save

      # if the deployed_application is created associate the current user with the brigade that
      # deployed the application
      @deployed_application.brigade.users << current_user if @deployed_application.brigade.present?
      redirect_to @deployed_application, notice: 'The application was deployed successfully!'
    else
      flash[:alert] = 'The application could not be deployed'

      @location = Location.new
      @brigade = Brigade.new
      render :new
    end
  end
end
