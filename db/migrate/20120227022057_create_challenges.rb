class CreateChallenges < ActiveRecord::Migration
  def change
    create_table :challenges do |t|
      t.text  :description

      t.timestamp
    end
  end
end
