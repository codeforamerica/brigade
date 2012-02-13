class AddIrcChannelTwitterHashtagDescriptionToApplications < ActiveRecord::Migration
  def change
    add_column :applications, :irc_channel, :string
    add_column :applications, :twitter_hashtag, :string
    add_column :applications, :description, :text

  end
end
