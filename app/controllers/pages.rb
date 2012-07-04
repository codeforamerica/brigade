class PagesController < Devise::RegistrationsController

  layout 'pages'

  def index
    @user ||= User.new
  end
end
