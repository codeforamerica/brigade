require 'code-for-america/github_omniauth_parser'

class RegistrationsController < Devise::RegistrationsController

  def new
    build_user
  end

  def new_organizer
    build_user
  end

  
  def create
    if params[:user][:password].blank?
      # from: http://blog.logeek.fr/2009/7/2/creating-small-unique-tokens-in-ruby
      params[:user][:password] = rand(36**8).to_s(36)
    end
    params[:user][:password_confirmation] = params[:user][:password]

    if session["devise.github_data"]
      parser = CodeForAmerica::GithubOmniAuthParser.new session["devise.github_data"]
      params[:user][:github_uid] = parser.github_uid
    end

    super

    if @user.persisted?
      KM.record('User Signup')
      KM.identify(@user.email)

      if params[:source] == "open_impact"
        SignupMailer.open_impact_greeting(@user).deliver
      else
        SignupMailer.greeting(@user).deliver
      end

      session["devise.github_data"] = nil
    end
  end

  private

  def build_user
    @user ||= User.new
  end

 end
