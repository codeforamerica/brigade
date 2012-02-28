class Brigade < ActiveRecord::Base
  has_many :deployed_applications
  has_many :applications, through: :deployed_applications

  has_and_belongs_to_many :users

  validates :name, presence: true

  def to_s
    name
  end
end
