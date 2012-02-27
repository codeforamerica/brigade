class Location < ActiveRecord::Base
  has_many :deployed_applications
  has_many :users
  has_many :challenges

  validates :name, uniqueness: true, presence: true

  def to_s
    name
  end
end
