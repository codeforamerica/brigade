Given /^I am on the homepage$/ do
  visit root_path
end

Then /^show me the page$/ do
  save_and_open_page
end

Given /^I follow the "([^"]*)" link$/ do |link|
  click_on link
end
