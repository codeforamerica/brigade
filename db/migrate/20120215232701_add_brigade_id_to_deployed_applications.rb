class AddBrigadeIdToDeployedApplications < ActiveRecord::Migration
  def change
    add_column :deployed_applications, :brigade_id, :integer
  end
end
