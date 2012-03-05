class Location < ActiveRecord::Base
  has_many :deployed_applications
  has_many :users
  has_many :challenges

  geocoded_by :name

  validates :name, uniqueness: true, presence: true

  def self.names
    all.map(&:name)
  end

  def to_s
    name
  end
end
