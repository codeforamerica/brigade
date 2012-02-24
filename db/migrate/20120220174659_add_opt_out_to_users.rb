class AddOptOutToUsers < ActiveRecord::Migration
  def change
    add_column :users, :opt_out, :boolean, default: false

  end
end
