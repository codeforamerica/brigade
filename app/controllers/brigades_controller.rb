class BrigadesController < ApplicationController
  def find
    @brigade = Brigade.find_by_name params[:brigade]

    if @brigade
      redirect_to brigade_deployed_applications_path(@brigade)
    else
      redirect_to deployed_applications_path(filter_by: 'brigades'), notice: "There are no apps currently deployed by #{params[:brigade]}"
    end
  end
end
