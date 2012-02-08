class ApplicationsController < ApplicationController
  skip_before_filter :authenticate_user!

  def index
    @apps = Application.all
  end
end
