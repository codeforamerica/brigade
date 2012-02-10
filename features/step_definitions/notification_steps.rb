Then /^I am notified that the email field can't be blank$/ do
  page.should have_content "Email can't be blank"
end

Then /^I should be notified that I am signed in$/ do
  page.should have_content 'Successfully authorized from Github account'
end
