class AddLogoToApplications < ActiveRecord::Migration
  def change
    add_column :applications, :logo, :string, default: '('

  end
end
