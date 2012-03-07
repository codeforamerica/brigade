require 'code-for-america/github_omniauth_parser'

class RegistrationsController < Devise::RegistrationsController

  def new
    build_user
  end

  def create
    params[:user][:password_confirmation] = params[:user][:password]

    if session["devise.github_data"]
      parser = CodeForAmerica::GithubOmniAuthParser.new session["devise.github_data"]
      params[:user][:github_uid] = parser.github_uid
    end

    super

    session["devise.github_data"] = nil if @user.persisted?
  end

  private

  def build_user
    if session["devise.github_data"]

      parser = CodeForAmerica::GithubOmniAuthParser.new session["devise.github_data"]
      @user = User.new

      @user.github_uid = parser.github_uid
      @user.full_name = parser.name
      @user.email = parser.email
    end
    @user ||= User.new
  end

 end
