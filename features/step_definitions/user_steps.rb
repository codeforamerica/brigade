Given /^the following civic hackers exist:$/ do |table|
  table.hashes.each do |hash|

    location = Location.find_or_create_by_name(hash['Location'])
    brigade = Brigade.find_by_name(hash['Brigade'])

    unless brigade
      brigade = Brigade.create(name: hash['Brigade'], point_of_contact_address: 'testman@example.com')
    end

    user = FactoryGirl.create(:user, email: hash['Email'], brigade_ids: [brigade.id], location_id: location.id, skill_list: hash['Skills'])
  end
end

When /^I view all of the civic hackers$/ do
  visit('/')
  click_on 'People'
end

Then /^I should be preseneted with a list of all the civic hackers$/ do
  page.should have_content 'People hacking across the country'
end

When /^I search for all civic hackers who are working (?:on|with) "([^"]*)"$/ do |search_term|
  fill_in 'query', with: search_term
  click_on 'Search'
end

When /^I search for all civic hackers who have the skill "([^"]*)"$/ do |skill|
  step "I search for all civic hackers who are working on \"#{skill}\""
end

Then /^I should see a list of civic hackers that includes "([^"]*)"$/ do |email|
  user = User.find_by_email(email)
  page.should have_css "#user_#{user.id}", visible: true
end

Then /^I should be informed that there are no hackers who fit that criteria$/ do
  page.should have_content "There aren't any hackers that match that criteria!"
end

