class CreatePictures < ActiveRecord::Migration
  def change
    create_table :pictures do |t|
      t.string      :file
      t.references  :application

      t.timestamp
    end
  end
end
