class Application < ActiveRecord::Base

  has_many :tasks
  has_many :pictures

  has_many :deployed_applications
  has_many :participating_brigades, through: :deployed_applications, source: :brigade

  validates :nid, presence: true
  validates :logo, length: { in: 0..1 }
  validate :cannot_have_more_than_four_pictures

  def cannot_have_more_than_four_pictures
    if pictures.count > 4
      errors.add(:pictures, "cannot have more than four")
    end
  end

  def to_s
    name
  end

  def deployed_application_users
    users = Array.new

    deployed_applications.map(&:brigade).each do |brigade|
      users = users + brigade.users
    end

    users.uniq
  end
end
