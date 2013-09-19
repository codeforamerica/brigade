class BrigadesController < ApplicationController
  before_filter :authenticate_user!, only: [:join, :leave]
  respond_to :json, :html

  def find
    @brigade = Brigade.find_by_name params[:brigade]

    if @brigade
      redirect_to brigade_deployed_applications_path(@brigade)
    else
      redirect_to deployed_applications_path(filter_by: 'brigades'), notice: "There are no apps currently deployed by #{params[:brigade]}"
    end
  end

  def create
    @brigade = Brigade.new params[:brigade]

    if @brigade.save
      render json: @brigade, status: 200
    else
      render json: @brigade.errors, status: 400
    end
  end

  def index
    @brigades = Brigade.all(:order => 'name')
    respond_with(@brigades)
  end

  def show
    build_user
    build_location
    @source="brigade"

    @brigade_base = Brigade.find(params[:id], :include => :users)

    @brigade = BrigadeDecorator.new(@brigade_base)

    respond_to do |format|
      format.html
      format.json { render :json => @brigade_base.to_json(:include => {:users  => {:except => [:email, :opt_in, :admin, :updated_at]} }) }
    end

  end

  def join
    @brigade = Brigade.find params[:id]
    current_user.join_brigade(@brigade)
    params[:redirect_uri] ||= brigade_path(@brigade)
    redirect_to params[:redirect_uri]
  end

  def leave
    @brigade = Brigade.find params[:id]
    current_user.leave_brigade(@brigade)
    redirect_to brigade_url(@brigade)
  end
  
  def locations
    render json: Brigade.all
  end

  def application_locations
    render json: Brigade.find_by_id(params[:id]).deployed_applications
  end
  
  private 
  def build_user
    @user ||= User.new
  end
  def build_location
    @location ||= Location.new
  end

end
