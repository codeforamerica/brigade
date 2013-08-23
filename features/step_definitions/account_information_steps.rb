Then /^I edit my account information$/ do
  click_on 'Edit'

  fill_in 'user[skill_list]', with: 'Ruby, Java, Project Management'
  fill_in 'Enter your current password to make these changes', with: 'password'

  fill_in 'user[current_password]', with: 'password'
  click_on 'Update User'
end

Then /^I create a new location with a modal in the "([^"]*)" form$/ do |form_name|
  select "Add Location", from: "#{form_name}[location_id]"
  fill_in 'location[name]', with: 'Random Location'
  find_field('location[name]').value.should == 'Random Location'
  click_on 'Create Location'

  wait_until { Location.find_by_name('Random Location') }
end

When /^I create a new location "([^"]*)" in the location select box$/ do |location|
  click_on 'Edit'

  select "Add Location", from: "user[location_id]"
  fill_in 'location[name]', with: location
  find_field('location[name]').value.should == 'Random Location'
  click_on 'Create Location'

  wait_until { Location.find_by_name('Random Location') }
end

Then /^"([^"]*)" is available in the select box$/ do |location|
  Location.last.name.should == location
end

Then /^I see the updated information on my account page$/ do
  page.should have_content 'Does not want to be contacted by other civic hackers'
  page.should have_content 'Project Management, Java, Ruby'
end

Then /^I edit my account information and leave the select box on Add Location$/ do
  click_on 'Edit'

  select "Add Location", from: "user[location_id]"

  fill_in 'user[current_password]', with: 'password'
  click_on 'Update User'
end

Then /^I am on the show user page with no location$/ do
  page.current_path.should == "/members/#{User.last.id}"
  page.should_not have_content 'Add Location'
end

When /^I edit my email preferences$/ do
  click_on 'Edit'

  check 'user[opt_in]'

  fill_in 'user[current_password]', with: 'password'
  click_on 'Update User'
end

Then /^I see a clickable "([^"]*)" on my account page$/ do |email|
  page.should have_content email
end
