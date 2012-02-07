Given /^I successfully register with my email "([^"]*)"$/ do |email|
  fill_in "user[email]", with: email
  fill_in "user[password]", with: "password"
  fill_in "user[password_confirmation]", with: "password"

  click_on 'Sign up'
end

Then /^I am on my profile page$/ do
  page.should have_content 'testman@example.com'
end

Given /^I unsuccessfully register by not filling in my email$/ do
  fill_in "user[password]", with: "password"
  fill_in "user[password_confirmation]", with: "password"

  click_on 'Sign up'
end

Then /^I am notified that the email field can't be blank$/ do
  page.should have_content "Email can't be blank"
end
