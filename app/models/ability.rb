class Ability
  include CanCan::Ability

  def initialize(user)
    if user
      can :manage, DeployedApplication
    end
  end
end
