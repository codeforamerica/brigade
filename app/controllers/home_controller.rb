class HomeController < ApplicationController

  layout 'homepage'

  def index
    @user ||= User.new
  end
  
  def create
    puts "--------------------------------HERE--------------------------------"
    User.create! do |u|
      
      u.first_name = params[:input_name]
      u.email = params[:input_email]
      
      
    end
  end
  
end
