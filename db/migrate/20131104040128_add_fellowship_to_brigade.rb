class AddFellowshipToBrigade < ActiveRecord::Migration
  def change
    add_column :brigades, :fellowship, :string
  end
end
