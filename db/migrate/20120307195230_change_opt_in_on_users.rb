class ChangeOptInOnUsers < ActiveRecord::Migration
  def up
    rename_column :users, :opt_out, :opt_in
    change_column :users, :opt_in, :boolean, default: false
  end

  def down
    change_column :users, :opt_in, :boolean
    rename_column :users, :opt_in, :opt_out
  end
end
