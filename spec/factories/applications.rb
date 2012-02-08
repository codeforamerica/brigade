FactoryGirl.define do
  factory :application do
    name              'Titans App'
    repository_url    'https://github.com/wearetitans/code-for-america'
    irc_channel       '#brigade-channel'
    twitter_hashtag   '#brigade-hashtag'
    description       'Long winded description of application'
  end

  factory :application_with_tasks_and_brigades, parent: :application do

    after_create do |application|
      5.times do |n|
        FactoryGirl.create(:task, application_id: application.id)
        FactoryGirl.create(:deployed_application, application_id: application.id)
      end
    end
  end
end
