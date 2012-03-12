class Challenge < ActiveRecord::Base
  acts_as_taggable_on :technology_platforms

  belongs_to :location

  validates :purpose, presence: true
  validates :location, presence: true

  validates :organization_name, presence: true
  validates :description, presence: true

  state_machine :status, initial: :submitted do
    state :submitted
    state :accepted
    state :rejected
    state :idle
  end

  def self.state_names
    state_machines[:status].states.map(&:name)
  end

  def i_statement
    "I challenge #{location.name} to #{purpose}."
  end

  def self.publicly_visible_challenges
    Challenge.all.keep_if {|x| x.public_visibility == true}
  end

end
