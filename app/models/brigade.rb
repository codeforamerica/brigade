class Brigade < ActiveRecord::Base
  has_many :deployed_applications
  has_many :applications, through: :deployed_applications
  
  belongs_to :location
  
  has_and_belongs_to_many :users

  validates :name, presence: true
  validates_uniqueness_of :name, :case_sensitive => false
  validates :point_of_contact_address, presence: true

  serialize :meetup_json_data, JSON

  def to_s
    name
  end
  
  def as_json(options={})
    super(include: [:location])
  end

  def remove_img_tags
    self.delete!(/^(<img.*?)>/)
  end

end
