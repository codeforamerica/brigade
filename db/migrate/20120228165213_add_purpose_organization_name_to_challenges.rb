class AddPurposeOrganizationNameToChallenges < ActiveRecord::Migration
  def change
    add_column :challenges, :purpose, :string
    add_column :challenges, :organization_name, :string

  end
end
