class UsersController < ApplicationController
  load_and_authorize_resource

  def show
    @user = UserDecorator.new(User.find(params[:id]))
  end

  def edit
    @user = UserDecorator.new(User.find(params[:id]))
    @location = Location.new
  end

  def update
    @user = User.find(params[:id])

    if @user.update_attributes(params[:user])
      redirect_to user_path(@user)
    else
      render :edit
    end
  end

  def index
    session[:query] = params[:query] if params[:query]

    @search = User.search do
      fulltext session[:query]
    end

    @users = @search.results
  end
end
