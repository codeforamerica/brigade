class CreateBrigadesUsers < ActiveRecord::Migration
  def change
    create_table :brigades_users, :id => false  do |t|
      t.references :user
      t.references :brigade
    end
  end
end
