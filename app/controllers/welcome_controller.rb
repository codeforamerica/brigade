class WelcomeController < ApplicationController
  
  
  
  def brigade
    set_brigade
  end
  
  
  private
  
  def set_brigade
    @brigade = Brigade.find(params[:id])
  end
end

