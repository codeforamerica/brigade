class ChallengeMailer < ActionMailer::Base
  default from: "no-reply@codeforamerica.org"

  def notify_of_submitted_challenge(challenge)
    @challenge = challenge
    mail(to: "brigade-info@codeforamerica.org", subject: "Challenge ##{challenge.id} Submitted")
  end
end
