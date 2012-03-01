require "spec_helper"

describe ChallengeMailer do

  before do
    @challenge = FactoryGirl.create(:challenge)
    @email = ChallengeMailer.notify_of_submitted_challenge(@challenge)
  end

  it "sets the sender to \'no-reply@codeforamerica.com\'" do
    @email.should deliver_from "no-reply@codeforamerica.org"
  end

  it "includes the challenge number in the subject" do
    @email.should have_subject "Challenge ##{@challenge.id} Submitted"
  end

  it "includes a link to the rails admin show challenge page" do
    @email.should have_body_text "#{root_url}admin/challenge/#{@challenge.id}"
  end
end
