class HomeController < ApplicationController

  layout 'homepage-new'

  def index
    @user ||= User.new
  end


end