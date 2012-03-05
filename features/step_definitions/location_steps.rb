Given /^I live in "([^"]*)"$/ do |location_name|
  Location.create!(name: location_name)
end

When /^I decide that I want to start hacking in "([^"]*)"$/ do |city|
  visit('/')
  fill_in 'location', with: city
  click_on 'Let\'s go!'
end
