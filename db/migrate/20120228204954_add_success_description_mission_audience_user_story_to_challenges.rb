class AddSuccessDescriptionMissionAudienceUserStoryToChallenges < ActiveRecord::Migration
  def change
    add_column :challenges, :success_description, :string
    add_column :challenges, :mission, :text
    add_column :challenges, :audience, :text
    add_column :challenges, :user_story, :text

  end
end
