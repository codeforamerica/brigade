class AddLocationToDeployedApplications < ActiveRecord::Migration
  def change
    add_column :deployed_applications, :location, :string
  end
end
