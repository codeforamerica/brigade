require 'spec_helper'

describe ChallengesController do
	describe "POST #create" do
		context "with valid attributes" do
			before(:each) do
		  	@challenge = FactoryGirl.build_stubbed(:challenge)
		  	@challenge.stub(:save) {true}
		  	Challenge.stub(:new) {@challenge}
			end
			it "saves the new challenge in the database" do
				@challenge.should_receive :save
				post :create, challenge: @challenge.attributes
			end
			it "notifies the CfA staff via email of the newly submitted challenge" do
				mailer = mock
				mailer.should_receive(:deliver)
				ChallengeMailer.should_receive(:notify_of_submitted_challenge).with(@challenge).and_return(mailer)
				post :create, challenge: @challenge.attributes
			end
			it "notifies the user of the challenge creation via the flash" do
				post :create, challenge: @challenge.attributes
				flash[:notice].should eq('Challenge submitted to Code for America staff')
			end
			it "redirects to the home page" do
				post :create, challenge: @challenge.attributes
				response.should redirect_to root_path
			end
		end 
		context "with invalid attributes" do
			before(:each) do
				@challenge = FactoryGirl.build_stubbed(:challenge)
		  	@challenge.stub(:save) {false}
		  	Challenge.stub(:new) {@challenge}
		  	@location = FactoryGirl.build_stubbed(:location)
		  	Location.stub(:new) {@location}
			end 
			it "attempts to save the new challenge in the database" do
				@challenge.should_receive :save
				post :create, challenge: @challenge.attributes
			end
			it "does not notify the CfA staff via email of the newly submitted challenge" do
				ChallengeMailer.should_not_receive(:notify_of_submitted_challenge).with(@challenge)
				post :create, challenge: @challenge.attributes
			end
			it "does not notify the user of the challenge creation via the flash" do
				post :create, challenge: @challenge.attributes
				flash[:notice].should be_nil
			end
			it "redirects to the home page" do
				post :create, challenge: @challenge.attributes
				response.should_not redirect_to root_path
			end
			it "assigns a new location instance" do
			  post :create, challenge: @challenge.attributes
			  assigns(:location).should eq(@location)
			end
			it "re-renders the :new template" do
				post :create, challenge: @challenge.attributes
				response.should render_template :new
			end
		end 
	end
end