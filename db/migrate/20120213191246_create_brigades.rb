class CreateBrigades < ActiveRecord::Migration
  def change
    create_table :brigades do |t|
      t.references :deployed_application
      t.string :name

      t.timestamps
    end
  end
end
