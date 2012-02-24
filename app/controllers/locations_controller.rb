class LocationsController < ApplicationController

  def find
    @location = Location.find_by_name params[:location]

    if @location
      redirect_to location_deployed_applications_path(@location)
    else
      redirect_to deployed_applications_path(filter_by: 'locations'), notice: "There are no apps currently deployed in #{params[:location]}"
    end
  end

  def create
    @location = Location.new params[:location]

    if @location.save
      render json: @location, status: 200
    else
      render json: @location.errors, status: 400
    end
  end
end
