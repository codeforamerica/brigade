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
    click_on 'People'
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
