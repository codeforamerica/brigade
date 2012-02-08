class CreateApplications < ActiveRecord::Migration
  def change
    create_table :applications do |t|
      t.string :name

      t.timestamp
    end
  end
end
