class Ability
  include CanCan::Ability

  def initialize(user)
    if user
      can :manage, DeployedApplication
      can :manage, Challenge
    end
  end
end
