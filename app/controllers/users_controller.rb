class UsersController < ApplicationController
  NUM_PER_PAGE = 50
  respond_to :json, :html

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
    page = params[:page] || 1

    if params[:query]
      @search = User.search do
        fulltext params[:query]
        paginate :page => page, :per_page => NUM_PER_PAGE
      end
      @users = @search.results
      @count = @search.total
    else
      @users = User.includes(:location).page(page).per(NUM_PER_PAGE)
      @count = User.count
    end
    respond_to do |format|
      format.html
      format.json { render :json => @users.to_json(:except => [:email, :opt_in, :admin, :updated_at]) }
    end

  end

  def destroy
    user = User.find(params[:id])
    if user == current_user && user.destroy
      redirect_to :root
    else
      redirect_to user_path(@user)
    end
  end

end
