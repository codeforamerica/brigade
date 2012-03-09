class Ability
  include CanCan::Ability

  def initialize(user)

    can :read, User

    if user
      can :manage, User, {id: user.id}
      can :manage, DeployedApplication
      can :manage, Challenge

      can :leave, Brigade do |b|
        user.is_member_of?(b)
      end

    end
  end
end
