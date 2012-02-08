class ApplicationsController < ApplicationController

  def index
    @apps = Application.all
  end
end
