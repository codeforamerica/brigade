class User < ActiveRecord::Base
  mount_uploader :avatar, PictureUploader

  acts_as_taggable_on :skills

  # Include default devise modules. Others available are:
  # :token_authenticatable, :encryptable, :confirmable, :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable, :registerable, :omniauthable,
         :recoverable, :rememberable, :trackable, :validatable

  # Setup accessible (or protected) attributes for your model
  attr_accessible :email, :password, :password_confirmation, :remember_me,
                  :opt_out, :location_id, :avatar, :skill_list

  belongs_to :location
  delegate :name, to: :location, prefix: true, allow_nil: true

  has_and_belongs_to_many :brigades
  has_many :applications, through: :brigades

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

  def self.find_for_github_oauth(access_token, signed_in_resource=nil)
    email = access_token.info.email.downcase

    if user = User.where(:email => email).first
      user
    else # Create a user with a stub password.
      User.create!(:email => email, :password => Devise.friendly_token[0,20])
    end
  end
end
