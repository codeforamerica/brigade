Given /^I live in "([^"]*)"$/ do |location_name|
  Location.create!(name: location_name)
end
