require 'code-for-america/github_omniauth_parser'

class Users::OmniauthCallbacksController < Devise::OmniauthCallbacksController

  def github

    parser = CodeForAmerica::GithubOmniAuthParser.new request.env["omniauth.auth"]
    email = parser.email
    github_uid = parser.github_uid
    name = parser.name

    # You need to implement the method below in your model
    user = current_user || User.find_or_create_by_email_and_github_uid(email, name, github_uid)

    if user.persisted?
      user.update_github_uid(github_uid)
      flash[:notice] = I18n.t "devise.omniauth_callbacks.success", :kind => "Github"
      sign_in_and_redirect user, :event => :authentication
    else
      session["devise.github_data"] = request.env["omniauth.auth"]
      redirect_to new_user_registration_url
    end
  end
end
