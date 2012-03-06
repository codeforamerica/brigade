FactoryGirl.define do
  factory :brigade do
    sequence(:name) { |n| "#{n} Brigade Name" }

    point_of_contact_address     "testmant@googlegroups.com"
  end
end
