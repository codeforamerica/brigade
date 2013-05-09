class AddLinkedinUrlToUsers < ActiveRecord::Migration
  def change
    add_column :users, :linkedin_url, :string
  end
end
