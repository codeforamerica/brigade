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

  def location_name
    'Test'
  end

  def self.find_for_github_oauth(access_token, signed_in_resource=nil)
    data = access_token.extra.raw_info

    if user = User.where(:email => data.email.downcase).first
      user
    else # Create a user with a stub password.
      User.create!(:email => data.email, :password => Devise.friendly_token[0,20])
    end
  end
end
