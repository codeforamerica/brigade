class User < ActiveRecord::Base

  acts_as_taggable_on :skills

  # Include default devise modules. Others available are:
  # :token_authenticatable, :encryptable, :confirmable, :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable, :registerable, :omniauthable,
         :recoverable, :rememberable, :trackable, :validatable

  # Setup accessible (or protected) attributes for your model
  attr_accessible :email, :password, :password_confirmation, :remember_me,
                  :opt_in, :location_id, :avatar, :skill_list, :avatar_cache, :github_uid,
                  :full_name, :first_name, :last_name

  validates :full_name, presence: true

  belongs_to :location
  delegate :name, to: :location, prefix: true, allow_nil: true

  has_and_belongs_to_many :brigades
  has_many :applications, through: :brigades

  scope :contactable, where(opt_in: true)

  searchable do
    text :email
    text :skill_list
    text :location_name

    text :brigade_names do
      brigades.map { |brigade| brigade.name }
    end

    text :application_names do
      applications.map { |application| application.name }
    end
  end

  def self.find_or_create_by_email_and_github_uid(email, name, github_uid)
    #This function is about finding a user from the github oauth hash or creating
    #one if one doesn't exist.

    #Try to find the user by github_id
    user = User.find_by_email(email) || User.find_by_github_uid(github_uid)

    user || User.create(email: email, github_uid: github_uid, full_name: name)
  end

  def update_github_uid(github_uid)
    update_attribute(:github_uid, github_uid)
  end

  def password_required?
    (github_uid.blank? || password.present?) && super
  end

  def full_name
    "#{first_name} #{last_name}" unless first_name.nil? and last_name.nil?
  end

  def full_name=(name)
    split = name.split(' ', 2)
    self.first_name = split.first
    self.last_name = split.last
  end

  alias :name :full_name

end
