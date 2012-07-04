class PagesController < ApplicationController

  layout 'pages'

  def index
    @user ||= User.new
  end
end
