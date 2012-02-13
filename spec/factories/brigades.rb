FactoryGirl.define do
  factory :brigade do
    sequence(:name) { |n| "#{n} Brigade Name" }
  end
end
