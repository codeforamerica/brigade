class AddNidCreatorShortDescriptionLicenseCivicCommonsDescriptionToApplications < ActiveRecord::Migration
  def change
    add_column :applications, :nid, :string
    add_column :applications, :creator, :string
    add_column :applications, :short_description, :string
    add_column :applications, :license, :string
    add_column :applications, :civic_commons_description, :text
  end
end
