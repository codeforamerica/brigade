class Application < ActiveRecord::Base

  validates :name, presence: true

end
