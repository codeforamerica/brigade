Then /^I can see the number of deploys that the application has$/ do
  page.should have_content Application.last.deployed_applications.count
end
