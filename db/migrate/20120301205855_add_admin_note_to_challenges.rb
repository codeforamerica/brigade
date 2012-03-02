class AddAdminNoteToChallenges < ActiveRecord::Migration
  def change
    add_column :challenges, :admin_note, :text

  end
end
