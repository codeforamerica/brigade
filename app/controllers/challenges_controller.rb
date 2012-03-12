class ChallengesController < ApplicationController

  def new
    @challenge = Challenge.new
    @location = Location.new

    authorize! :create, @challenge
  end

  def create
    @challenge = Challenge.new(params[:challenge])

    if @challenge.save
      ChallengeMailer.notify_of_submitted_challenge(@challenge).deliver

      flash[:notice] = 'Challenge submitted to Code for America staff'
      redirect_to root_path
    else
      @location = Location.new
      render :new
    end
  end

  def index
    @challenges = Challenge.publicly_visible_challenges
  end
end
