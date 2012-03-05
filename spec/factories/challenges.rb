FactoryGirl.define do
  factory :challenge do

    purpose                     'I do this because I should'
    organization_name           'We are Titans'
    description                 'We need to fix the heat'
    success_description         'This is what success looks like'

    technology_platform_list    'Ruby, Rails'
    location
  end
end
