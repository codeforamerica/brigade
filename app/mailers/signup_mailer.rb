class SignupMailer < ActionMailer::Base
  default from: "brigade-info@codeforamerica.org"
  
  def greeting(user)
    @user = user
    mail(to: user.email, subject: "Welcome to the CfA Brigade!")
  end
end
