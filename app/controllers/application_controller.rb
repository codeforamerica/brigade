class ApplicationController < ActionController::Base
  before_filter :authenticate_user!
  protect_from_forgery

  protected

  def after_sign_in_path_for(user)
    user_path(user)
  end
end
