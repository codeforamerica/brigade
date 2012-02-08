FactoryGirl.define do
  factory :task do
    sequence(:description) { |n| "#{n} Some long winded step description" }
  end
end
