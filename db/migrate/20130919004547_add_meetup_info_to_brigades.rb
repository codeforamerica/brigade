class AddMeetupInfoToBrigades < ActiveRecord::Migration
  def change
  	add_column :brigades, :meetup_url, :string
  	add_column :brigades, :meetup_json_data, :text
  end
end
