Given /^the following apps have been created$/ do |table|
  table.hashes.map do |hash|
    Factory(:application, name: hash['Name'])
  end
end

Then /^I see a directory of the following apps$/ do |table|
  table.hashes.map do |hash|
    page.should have_content hash['Name']
  end
end
