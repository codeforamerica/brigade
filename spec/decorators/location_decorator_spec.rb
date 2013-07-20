require 'spec_helper'

describe LocationDecorator do
  let(:decorator) { LocationDecorator.new(location) }
  let(:location) { double(:location, users: users) }
  describe "#decorated_members" do
    context "the location has users" do
      let(:user) { double(:user) }
      let(:user_decorator) { double(:user_decorator) }
      let(:users) { double(:users, uniq: [user]) }

      it "builds a user link for each user" do
        UserDecorator.should_receive(:new).with(user).and_return(user_decorator)
        user_decorator.should_receive(:as_link)
        decorator.decorated_members
      end
    end

    context "the location has no users" do
      let(:users) { [] }
      let(:helper) { double(:helper) }
      let(:tag) { double(:tag) }

      before do
        decorator.stub(:h) { helper }
        helper.stub(:content_tag) { tag }
      end

      it "returns explanation that location has no users" do
        helper.should_receive(:content_tag).with(:i, 'There are currently no users participating')
        decorator.decorated_members
      end
    end
  end
end
