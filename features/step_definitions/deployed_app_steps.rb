Given /^the following apps have been deployed:$/ do |table|
  table.hashes.each do |hash|
    app =  Application.find_by_name(hash['App Name']) || FactoryGirl.create(:application, name: hash['App Name'])

    brigade = Brigade.find_by_name(hash['Brigade']) || FactoryGirl.create(:brigade, name: hash['Brigade'])

    location = Location.find_by_name(hash['City']) || FactoryGirl.create(:location, name: hash['City'])

    FactoryGirl.create(:deployed_application, application: app, location: location, brigade: brigade)
  end
end

When /^I view all of the apps by "([^"]*)"$/ do |type|
  visit ('/')

  if type == 'Brigade'
    click_on 'Brigades'
  else
    click_on 'Cities'
  end
end

Then /^I should see the following applications:$/ do |table|
  table.hashes.each do |hash|
    app = Application.find_by_name hash['App Name']
    brigade = Brigade.find_by_name hash['Brigade']

    deployed_app = DeployedApplication.find_by_application_id_and_brigade_id(app.id, brigade.id)

    within "#deployed_application_#{deployed_app.id}" do
      page.should have_content "#{hash['App Name']}"
      page.should have_content "#{hash['Brigade']}"
    end
  end
end

Then /^I should not see the following applications:$/ do |table|
  table.hashes.each do |hash|
    app = Application.find_by_name hash['App Name']
    brigade = Brigade.find_by_name hash['Brigade']
    location = Location.find_by_name hash['City']

    deployed_app = DeployedApplication.find_by_application_id_and_brigade_id_and_location_id(app.id, brigade.id, location.id)

    page.should_not have_css("#deployed_application_#{deployed_app.id}")
  end
end

When /^I filter the deployed apps to only those that have been deployed in "([^"]*)"$/ do |city|
  fill_in 'City', with: city
  click_on 'Search'
end

When /^I filter the deployed apps to only those that have been deployed by "([^"]*)"$/ do | brigade|
  fill_in 'Brigade', with: brigade
  click_on 'Search'
end

Then /^I should be informed that there are no applications deployed in "([^"]*)"$/ do |city_name|
  page.should have_content "There are no apps currently deployed in #{city_name}"
end

Then /^I should be informed that there are no applications deployed by "([^"]*)"$/ do |brigade_name|
  page.should have_content "There are no apps currently deployed by #{brigade_name}"
end

When /^I search for all applications named "([^"]*)"$/ do |application_name|
  fill_in 'query', with: application_name
  click_on 'Search'
end

When /^I choose to deploy "([^"]*)"$/ do |application_name|
  step "I visit the application \"#{application_name}\" page"

  click_on "Deploy This App"
end

Then /^I should be presented with a form that lets me deploy "([^"]*)"$/ do |application_name|
  application = Application.find_by_name application_name

  page.current_path.should == new_application_deployed_application_path(application)
end

When /^I successfully deploy the application "([^"]*)"$/ do |application_name|
  step "I choose to deploy \"#{application_name}\""

  select 'Norfolk, VA', from: 'deployed_application[location_id]'
  select 'Test Brigade', from: 'deployed_application[brigade_id]'

  click_on 'Deploy This Application!'
end

When /^I specify a new brigade "([^"]*)"$/ do |brigade_name|
  # I don't really want to put this step here but I haven't figured out why Joe
  # calls this step again.  Maybe its a race condition? - RMC
  step "I choose to deploy \"First App\""

  select 'Add Brigade', from: 'deployed_application[brigade_id]'

  fill_in 'brigade[name]', with: brigade_name
  fill_in 'brigade[point_of_contact_address]', with: 'poc@example.com'
  click_on 'Create Brigade'

  wait_until { Brigade.find_by_name(brigade_name) }

  select 'Norfolk, VA', from: 'deployed_application[location_id]'

  click_on 'Deploy This Application!'
end

When /^I unsuccessfully deploy the application "([^"]*)"$/ do |application_name|
  step "I choose to deploy \"#{application_name}\""

  select 'Test Brigade', from: 'deployed_application[brigade_id]'

  click_on 'Deploy This Application!'
end

Then /^I should be informed that the application was not deployed$/ do
  page.should have_content 'The application could not be deployed'
end

Then /^I should be informed that the application "([^"]*)" was deployed successfully by "([^"]*)" in "([^"]*)"$/ do |application_name, brigade, location|
  page.should have_content 'The application was deployed successfully!'

  page.should have_content application_name
  page.should have_content location
  page.should have_content brigade
end

Then /^I should be able to deploy another application if I choose$/ do
  page.should have_link 'Deploy new application'
end

When /^I click the button to share the deployed application$/ do
  click_on 'Share'
end

Then /^I should be able to share with my facebook and twitter networks$/ do
  page.should have_content 'facebook'
  page.should have_content 'twitter'
end

Given /^a deployed application exists with the name "([^"]*)"$/ do |name|
  FactoryGirl.create(:deployed_application, name: name)
end

When /^I view the last deployed app page/ do
    da = DeployedApplication.last
    visit deployed_application_url(da)
end

Then /^I should see the last deployed application's name/ do
    da = DeployedApplication.last
    page.should have_content da.application.name
end
