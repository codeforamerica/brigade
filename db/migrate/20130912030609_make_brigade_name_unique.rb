class MakeBrigadeNameUnique < ActiveRecord::Migration
  def up
    add_index :brigades, [:name], :unique => true, :name => :unique_brigade_name
  end

  def down
    remove_index :brigades, :name => :unique_brigade_name
  end
end
