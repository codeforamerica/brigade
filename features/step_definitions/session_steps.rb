Given /^I have previously registered for an account$/ do
  step "I am on the homepage"
  step "I follow the \"Get Started\" link"
  step "I successfully register with my email \"testman@example.com\""

  click_on 'Sign Out'
end

Given /^I want to access my account$/ do
  click_on 'Sign In'
end

When /^I correctly fill in my email "([^"]*)" and password "([^"]*)"$/ do |email, password|
  fill_in "user[email]", with: email
  fill_in "user[password]", with: password

  click_on 'Sign in'
end

When /^I incorrectly fill in my log in credentials$/ do
  fill_in "user[email]", with: "random@email.com"
  fill_in "user[password]", with: "randompassword"

  click_on 'Sign in'
end

Then /^I should be informed that my log in was unsucessfull and I need to try again$/ do
  page.should have_content "Invalid email or password"
end
