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

    result = false
    result = @user.update_with_password(params[:user]) unless @user.github_uid.present?
    result = @user.update_without_password(params[:user]) if @user.github_uid.present?

    if result
      sign_in(@user, :bypass => true)
      redirect_to user_path(@user)
    else
      @user = UserDecorator.new(@user)
      @location = @user.location || Location.new
      render :edit
    end
  end

  def index
    @search = User.search do
      fulltext params[:query]
    end

    @users = @search.results
  end
end
