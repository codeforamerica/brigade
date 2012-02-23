class Brigade < ActiveRecord::Base
  has_many :deployed_applications

  validates :name, presence: true

  def to_s
    name
  end
end
