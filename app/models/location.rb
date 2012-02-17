class Location < ActiveRecord::Base
  has_many :deployed_applications

end
