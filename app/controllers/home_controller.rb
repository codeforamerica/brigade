class HomeController < ApplicationController

  layout 'homepage'

  def index
    @user ||= User.new
  end


end