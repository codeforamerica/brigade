class ApplicationController < ActionController::Base
  include Errship::Rescuers
  include Errship::ActiveRecord::Rescuers

  protect_from_forgery

  rescue_from CanCan::AccessDenied do |exception|
    flash[:error] = "Access denied."
    redirect_to root_url
  end

  protected

  def after_sign_in_path_for(user)
    if user.admin?
      rails_admin_path
    else
      request.env['omniauth.origin'] || stored_location_for(user) || user_path(user)
    end
  end
end
