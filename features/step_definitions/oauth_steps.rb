Then /^I can sign up using "([^"]*)"/ do |oauth_provider|
  page.should have_link "Sign up with #{oauth_provider}"
end

When /^I sign up using "([^"]*)"/ do |oauth_provider|
  click_on "Sign up with #{oauth_provider}"
end
