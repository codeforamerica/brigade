class DeployedApplication < ActiveRecord::Base
  belongs_to :application
  has_one :brigade
end
