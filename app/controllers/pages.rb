class PagesController < HighVoltage::PagesController #Devise::RegistrationsController HighVoltage::PagesController

  def index
    @user ||= User.new
  end
end
