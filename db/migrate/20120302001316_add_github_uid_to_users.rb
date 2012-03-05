class AddGithubUidToUsers < ActiveRecord::Migration
  def change
    add_column :users, :github_uid, :string
  end
end
