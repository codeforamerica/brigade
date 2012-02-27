class AddVideoEmbedCodeToApplications < ActiveRecord::Migration
  def change
    add_column :applications, :video_embed_code, :text
  end
end
