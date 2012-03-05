class AddPointOfContactAddressToBrigades < ActiveRecord::Migration
  def change
    add_column :brigades, :point_of_contact_address, :string
  end
end
