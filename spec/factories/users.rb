FactoryGirl.define do
  factory :user do
    full_name         "Test Man"
    sequence(:email)  { |n| "testman#{n}@example.com" }
    password          "password"

    skill_list 'random, foo, ruby'
  end
end
