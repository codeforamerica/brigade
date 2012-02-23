Given /^I belong to the brigade "([^"]*)"$/ do |brigade_name|
  Brigade.create!(name: brigade_name)
end
