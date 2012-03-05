class DeployedApplication < ActiveRecord::Base
  belongs_to :application
  delegate :name, to: :application

  belongs_to :location
  delegate :name, to: :location, prefix: true
  accepts_nested_attributes_for :location

  belongs_to :brigade
  delegate :name, to: :brigade, prefix: true
  accepts_nested_attributes_for :brigade

  validates :location, presence: true
  validates :brigade, presence: true

  def self.search(query = nil)
    if query
      joins(:brigade, :application).where("brigades.name ILIKE ? OR applications.name ILIKE ?", "%#{query}%","%#{query}%" )
    else
      all
    end
  end
end
