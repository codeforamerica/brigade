Then /^I can sign up using "([^"]*)"/ do |oauth_provider|
  page.should have_link "Sign up with #{oauth_provider}"
end

When /^I sign up using "([^"]*)"/ do |oauth_provider|
  click_on "Sign up with #{oauth_provider}"
end

Given /^I have a github account that has a public email address listed$/ do
  OmniAuth.config.mock_auth[:github] = OmniAuth::AuthHash.new({
    "provider"=>"github",
     "uid"=>1489336,
     "info"=>
      {"nickname"=>"titans-tester",
       "email"=>"testman@example.com",
       "name"=>"Titans Tester",
       "urls"=>{"GitHub"=>"https://github.com/titans-tester", "Blog"=>nil}
      }
    })
end

Given /^I have a github account that doesn't have a public email address listed$/ do
  OmniAuth.config.mock_auth[:github] = OmniAuth::AuthHash.new({
    "provider"=>"github",
     "uid"=>1489336,
     "info"=>
      {"nickname"=>"titans-tester",
       "email"=> nil,
       "name"=>"Titans Tester",
       "urls"=>{"GitHub"=>"https://github.com/titans-tester", "Blog"=>nil}
      }
    })
end

When /^I fill in my email address, "([^"]*)", when prompted$/ do |email|
  fill_in "user[email]", with: email
  click_on 'Sign up'
end
