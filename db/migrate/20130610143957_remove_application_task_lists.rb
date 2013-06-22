class RemoveApplicationTaskLists < ActiveRecord::Migration
  def up
    drop_table :tasks
  end

  def down
    create_table :tasks do |t|
      t.text    "description"
      t.integer "application_id"
    end
  end
end
