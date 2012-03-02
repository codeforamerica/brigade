When /^I fill out a challenge form$/ do
  click_on 'Submit a challenge'

  fill_in 'challenge[purpose]', with: 'This answers the why'
  fill_in 'challenge[organization_name]', with: 'We Are Titans'
  fill_in 'challenge[mission]', with: 'Long mission description'
  fill_in 'challenge[audience]', with: 'Description of their primary audience'
  fill_in 'challenge[description]', with: 'This is a code for america challenge'
  fill_in 'challenge[technology_platform_list]', with: 'Ruby, Rails'
  fill_in 'challenge[success_description]', with: 'Success is a successful demo'
  fill_in 'challenge[user_story]', with: 'This is a brief description of a user case'

  step "I create a new location with a modal in the \"challenge\" form"

  click_on 'Create Challenge'
end

Then /^I am notified that my challenge has been sent to the CfA staff$/ do
  page.should have_content 'Challenge submitted to Code for America staff'
end

And /^the CfA staff receives an email notification with my challenge$/ do
  step "\"brigade-info@codeforamerica.org\" should receive an email"
end
