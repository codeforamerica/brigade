Given /^that the location "([^"]*)" has been defined$/ do |location|
  FactoryGirl.create(:location, name: location)
end

When /^I fill out a challenge form$/ do
  click_on 'Submit a challenge'

  fill_in 'challenge[purpose]', with: 'This answers the why'
  fill_in 'challenge[organization_name]', with: 'We Are Titans'
  fill_in 'challenge[description]', with: 'This is a code for america challenge'

  click_on 'Create Challenge'
end

Then /^I am notified that my challenge has been sent to the CfA staff$/ do
  page.should have_content 'Challenge submitted to Code for America staff'
end

And /^the CfA staff receives an email notification with my challenge$/ do
  step "\"brigade-info@codeforamerica.org\" should receive an email"
end
