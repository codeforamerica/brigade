class Ability
  include CanCan::Ability

  def initialize(user)
    can :manage, DeployedApplication
  end
end
