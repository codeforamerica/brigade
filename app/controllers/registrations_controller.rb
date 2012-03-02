require 'code-for-america/github_omniauth_parser'

class RegistrationsController < Devise::RegistrationsController

  def create
    params[:user][:password_confirmation] = params[:user][:password]

    super
  end

  private

  def build_resource(*args)
    super
    if session["devise.github_data"]

      parser = CodeForAmerica::GithubOmniAuthParser.new session["devise.github_data"]

      @user.github_uid = parser.github_uid
      @user.valid?
    end
  end
end
