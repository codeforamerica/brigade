class AddDeployedUrlToDeployedApplication < ActiveRecord::Migration
  def change
    add_column :deployed_applications, :deployed_url, :string
  end
end
