class AddLocationToBrigades < ActiveRecord::Migration
  def change
    add_column :brigades, :location_id, :integer
  end
end
