class BrigadesController < ApplicationController
  before_filter :authenticate_user!, only: [:join, :leave]

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

  def show
    @brigade = BrigadeDecorator.new(Brigade.find(params[:id]))
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
end
