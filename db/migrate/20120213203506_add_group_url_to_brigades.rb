class AddGroupUrlToBrigades < ActiveRecord::Migration
  def change
    add_column :brigades, :group_url, :string

  end
end
