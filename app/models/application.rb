class Application < ActiveRecord::Base

  has_many :tasks
  has_many :pictures

  has_many :deployed_applications
  has_many :participating_brigades, through: :deployed_applications, source: :brigade

  validates :nid, presence: true
  validate :cannot_have_more_than_four_pictures

  def cannot_have_more_than_four_pictures
    if pictures.count > 4
      errors.add(:pictures, "cannot have more than four")
    end
  end

  def to_s
    name
  end
end
