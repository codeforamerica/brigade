class AddStatusAndPublicVisibilityToChallenges < ActiveRecord::Migration
  def change
    add_column :challenges, :status, :string
    add_column :challenges, :public_visibility, :boolean, default: false

  end
end
