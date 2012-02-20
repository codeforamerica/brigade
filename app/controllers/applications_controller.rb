class ApplicationsController < ApplicationController

  def index
    @apps = Application.all
  end

  def show
    @app = AppDecorator.new(Application.find(params[:id]))
  end
end
