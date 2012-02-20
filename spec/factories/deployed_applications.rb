FactoryGirl.define do
  factory :deployed_application do
    application
    brigade
    location
  end
end
