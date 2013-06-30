class SignupMailer < ActionMailer::Base
  default from: "brigade@codeforamerica.org"

  def greeting(user)
    @user = user
    mail(to: user.email, cc: ['brigade@codeforamerica.org'], subject: "Welcome to the Code for America Brigade!")
  end

  def open_impact_greeting(user)
    @user = user
    mail(to: user.email, cc: ['brigade@codeforamerica.org', 'openimpact@codeforamerica.org'], subject: "Welcome to The Open Impact Campaign!")
  end
end
