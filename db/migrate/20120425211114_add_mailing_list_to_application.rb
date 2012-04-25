class AddMailingListToApplication < ActiveRecord::Migration
  def change
    add_column :applications, :mailing_list, :string
  end
end
