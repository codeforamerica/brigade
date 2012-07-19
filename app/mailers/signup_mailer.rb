class SignupMailer < ActionMailer::Base
  default from: "brigade-info@codeforamerica.org"

  def greeting(user)
    @user = user
    mail(to: user.email, cc: ['kevin@codeforamerica.org', 'jack@codeforamerica.org'], subject: "Welcome to the Code for America Brigade!")
  end

  def open_impact_greeting(user)
    @user = user
    mail(to: user.email, cc: ['kevin@codeforamerica.org', 'jack@codeforamerica.org', 'openimpact@codeforamerica.org'], subject: "Welcome to The Open Impact Campaign!")
  end
end
