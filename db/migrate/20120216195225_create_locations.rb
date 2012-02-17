class CreateLocations < ActiveRecord::Migration
  def change
    create_table :locations do |t|
      t.string :name

      t.timestamp
    end

    change_table :deployed_applications do |t|
      t.remove :location
      t.references :location
    end
  end
end
