class DeployedApplication < ActiveRecord::Base
  belongs_to :application
  delegate :name, to: :application

  belongs_to :location
  delegate :name, to: :location, prefix: true
  accepts_nested_attributes_for :location

  belongs_to :brigade
  delegate :name, to: :brigade, prefix: true
  accepts_nested_attributes_for :brigade

  validates :location_id, presence: true, uniqueness: { scope: [:brigade_id, :application_id], message: "Brigade has already deployed this app in this location" }
  validates :brigade, presence: true
  validates :application, presence: true
end
