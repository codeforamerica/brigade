FactoryGirl.define do
  factory :picture do
    file    File.open("#{Rails.root}/app/assets/images/avatar.jpg")
  end
end
