class Application < ActiveRecord::Base

  validates :nid, presence: true

  has_many :tasks

  has_many :deployed_applications
  has_many :participating_brigades, through: :deployed_applications, source: :brigade
end
