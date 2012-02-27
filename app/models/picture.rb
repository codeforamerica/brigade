class Picture < ActiveRecord::Base
  mount_uploader :file, PictureUploader

end
