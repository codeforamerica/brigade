class AddDeployedToDeployedApplications < ActiveRecord::Migration
  def change
    add_column :deployed_applications, :deployed, :boolean, default: false

  end
end
