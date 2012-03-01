class AddLocationIdToChallenges < ActiveRecord::Migration
  def change
    add_column :challenges, :location_id, :integer

  end
end
