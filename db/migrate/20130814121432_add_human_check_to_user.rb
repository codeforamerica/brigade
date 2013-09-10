class AddHumanCheckToUser < ActiveRecord::Migration
  def change
    add_column :users, :human_check, :string
  end
end
