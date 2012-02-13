class AddRepositoryUrlToApplications < ActiveRecord::Migration
  def change
    add_column :applications, :repository_url, :string

  end
end
