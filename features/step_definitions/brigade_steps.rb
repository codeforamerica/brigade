Given /^I belong to the brigade "([^"]*)"$/ do |brigade_name|
  FactoryGirl.create(:brigade, name: brigade_name)
end
