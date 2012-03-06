Then /^I can see the number of deploys that the application has$/ do
  page.should have_content Application.last.deployed_applications.count
end

Then /^I should see the following undeployed applications:$/ do |table|
  table.hashes.each do |hash|
    app = Application.find_by_name hash['App Name']

    page.should have_css("#application_#{app.id}")
  end
end