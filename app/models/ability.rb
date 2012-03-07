class Ability
  include CanCan::Ability

  def initialize(user)
    can :read, User

    if user
      can :manage, User, {id: user.id}
      can :manage, DeployedApplication
      can :manage, Challenge
    end
  end
end
