class PagesController < HighVoltage::PagesController
  def show
    @user ||= User.new
    super
  end
end
