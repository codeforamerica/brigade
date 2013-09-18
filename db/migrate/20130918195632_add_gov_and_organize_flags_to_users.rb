class AddGovAndOrganizeFlagsToUsers < ActiveRecord::Migration
  def change
    add_column :users, :willing_to_organize, :boolean
    add_column :users, :work_in_government, :boolean
  end
end
