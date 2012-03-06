Given /^I belong to the brigade "([^"]*)"$/ do |brigade_name|
  FactoryGirl.create(:brigade, name: brigade_name)
end

Given /^a brigade exists with the name "([^"]*)"$/ do |brigade_name|
  FactoryGirl.create(:brigade, name: brigade_name)
end

When /^I view the brigade "([^"]*)"$/ do |brigade_name|
    brigade = Brigade.find_by_name(brigade_name)
    visit brigade_url(brigade)
end

Then /^I should see the brigade's name: "([^"]*)"$/ do |brigade_name|
    brigade = Brigade.find_by_name(brigade_name)
    page.should have_content brigade.name
end
