FactoryGirl.define do
  factory :user do
    full_name         "Test Man"
    sequence(:email)  { |n| "testman#{n}@example.com" }
    password          "password"
    human_check       ''
    skill_list        'random, foo, ruby'
  end
end
