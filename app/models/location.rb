class Location < ActiveRecord::Base
  has_many :deployed_applications
  has_many :users
  has_many :challenges

  geocoded_by :name

  validates :name, uniqueness: true, presence: true

  after_validation :geocode

  def applications_not_deployed
    Application.all - deployed_applications.map(&:application).uniq
  end

  def self.names
    all.map(&:name)
  end

  def to_s
    name
  end
end
