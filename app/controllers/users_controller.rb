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

    if @user.update_with_password(params[:user])
      sign_in(@user, :bypass => true)
      redirect_to user_path(@user)
    else
      @user = UserDecorator.new(@user)
      @location = @user.location || Location.new
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
