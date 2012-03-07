Then /^I edit my account information$/ do
  click_on 'Edit'

  fill_in 'user[skill_list]', with: 'Ruby, Java, Project Management'
  fill_in 'Enter your current password to make these changes', with: 'password'

  step "I create a new location with a modal in the \"user\" form"

  click_on 'Update User'
end

Then /^I create a new location with a modal in the "([^"]*)" form$/ do |form_name|
  select "Add Location", from: "#{form_name}[location_id]"
  fill_in 'location[name]', with: 'Random Location'
  find_field('location[name]').value.should == 'Random Location'
  click_on 'Create Location'

  wait_until { Location.find_by_name('Random Location') }
end

Then /^I see the updated information on my account page$/ do
  page.should have_content 'Does not want to be contacted by other civic hackers'
  page.should have_content 'Random Location'
  page.should have_content 'Project Management, Java, Ruby'
end

Then /^I edit my account information and leave the select box on Add Location$/ do
  click_on 'Edit'

  select "Add Location", from: "user[location_id]"

  click_on 'Update User'
end

Then /^I am on the show user page with no location$/ do
  page.current_path.should == '/users/1'
  page.should_not have_content 'Add Location'
end
