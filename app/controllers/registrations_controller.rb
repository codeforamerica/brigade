require 'code-for-america/github_omniauth_parser'

class RegistrationsController < Devise::RegistrationsController
  skip_before_filter :verify_authenticity_token

  def new
    build_user
    build_location
    set_source
  end
  
  def create
    build_location
    set_source
    if params[:brigade_id].present?
      @brigade = Brigade.find(params[:brigade_id])
    end
    if params[:user][:password].blank?
      # from: http://blog.logeek.fr/2009/7/2/creating-small-unique-tokens-in-ruby
      params[:user][:password] = rand(36**8).to_s(36)
    end
    params[:user][:password_confirmation] = params[:user][:password]

    if session["devise.github_data"]
      parser = CodeForAmerica::GithubOmniAuthParser.new session["devise.github_data"]
      params[:user][:github_uid] = parser.github_uid
    end

    if session["user_return_to"].blank?
      if(@source == "organizer")
        if params[:user][:willing_to_organize] == "false"
          @source = "no_brigade"
          session["user_return_to"] = "/welcome/notify"
        else
          session["user_return_to"] = "/welcome/organizer"
        end
      elsif(@source == "no_brigade")
        session["user_return_to"] = "/welcome/notify"
      elsif(@source == "brigade")
        if params[:brigade_id].present?
          session["user_return_to"] = "/welcome/brigade/"+params[:brigade_id]
        end
      else
        session["user_return_to"] = "/welcome"
      end
    end
    
    
    super

    if @user.persisted?
      KM.record('User Signup')
      KM.identify(@user.email)

      if params[:brigade_id].present?
        brigade = Brigade.find_by_id(params[:brigade_id])
        if brigade.present?
          @user.brigades << brigade
          @user.location = brigade.location
        end
        @user.save
      end

      
      
      if params[:source] == "open_impact"
        SignupMailer.open_impact_greeting(@user).deliver
      elsif @source == "brigade"
        SignupMailer.greeting_brigade(@user, @brigade).deliver
      elsif @source == "no_brigade"
        SignupMailer.greeting_no_brigade(@user).deliver
      elsif @source == "organizer"
        SignupMailer.greeting_organizer(@user).deliver
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
  def build_location
    @location ||= Location.new
  end
  def set_source
    if request.path == "/organize"
      @source = "organizer"
    elsif request.path == "/notify"
      @source = "no_brigade"
    else
      if(!params[:source].blank?)
        @source=params[:source]
      else
        @source = "base"
      end
    end
  end
 end
