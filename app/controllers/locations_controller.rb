class LocationsController < ApplicationController

  def find
    @location = Location.find_by_name params[:location]

    if @location
      redirect_to location_deployed_applications_path(@location)
    else
      if params[:location].empty?
        redirect_to root_path, alert: "A location name must be specified!"
      else
        redirect_to applications_path, notice: "No apps have been deployed to #{params[:location]}, deploy one today!"
      end
    end
  end

  def create
    @location = Location.new params[:location]

    if @location.save
      @location.geocode
      render json: @location, status: 200
    else
      render json: @location.errors, status: 400
    end
  end
end
