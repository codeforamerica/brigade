class RegistrationsController < Devise::RegistrationsController

  def create
    params[:user][:password_confirmation] = params[:user][:password]

    super
  end
end
