class Challenge < ActiveRecord::Base
  acts_as_taggable_on :technology_platforms

  belongs_to :location

  validates :purpose, presence: true
  validates :organization_name, presence: true
  validates :description, presence: true
  validates :location, presence: true
  validates :technology_platform_list, presence: true
  validates :success_description, presence: true

  state_machine :status, initial: :submitted do
    state :submitted
    state :accepted
    state :rejected
    state :idle
  end

  def self.state_names
    state_machines[:status].states.map(&:name)
  end

end
