class SignupMailer < ActionMailer::Base
  default from: "brigade-info@codeforamerica.org"

  def greeting(user)
    puts "HITTING THE MAILER"
    @user = user
    mail(to: user.email, subject: "Welcome to the CfA Brigade!")
  end
end
