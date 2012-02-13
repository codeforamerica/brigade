class CreateDeployedApplications < ActiveRecord::Migration
  def change
    create_table :deployed_applications do |t|
      t.references :application
      t.timestamps
    end
  end
end
