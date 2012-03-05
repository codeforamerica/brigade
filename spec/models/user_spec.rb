require 'spec_helper'

describe User do
  subject { Factory(:user) }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end

  it 'should be valid with an opt_out attribute' do
    subject.opt_out = true
    subject.should be_valid
  end

  context 'opt_out' do
    it 'should be false by default' do
      subject.opt_out.should == false
    end
  end

  describe '#location_name' do
    it 'knows the name of its location' do
      location = FactoryGirl.build(:location, name: 'Test')
      subject.location = location
      subject.location_name.should == 'Test'
    end
  end

  describe 'self.find_or_create_by_email_and_github_uid' do
    before do
      @email = 'testman@example.com'
      @github_uid = '123456'
    end

    context 'when a user already exists with the email address specified' do
      before do
        User.stub(:find_by_email).with(@email).and_return(subject)
      end

      it 'returns the user that was found' do
        User.find_or_create_by_email_and_github_uid(@email, @github_uid).should == subject
      end
    end

    context 'when a user already exists with the github_uid specified' do
      before do
        User.stub(:find_by_email).with(@email).and_return(nil)
        User.stub(:find_by_github_uid).with(@github_uid).and_return(subject)
      end

      it 'returns the user that was found' do
        User.find_or_create_by_email_and_github_uid(@email, @github_uid).should == subject
      end
    end

    context 'when no user exists with the email address or the github_uid specified' do
      before do
        User.stub(:find_by_email).with(@email).and_return(nil)
        User.stub(:find_by_github_uid).with(@github_uid).and_return(nil)
      end

      context 'when there is an email address included' do
        before do
          @user = User.find_or_create_by_email_and_github_uid(@email, @github_uid)
        end

        it 'creates a new user' do
          @user.should be_persisted
        end

        it 'should set the email address of the new user to the email specified' do
          @user.email.should == @email
        end

        it 'should set the github uid of the new user to the github_uid specified' do
          @user.github_uid.should == @github_uid
        end
      end

      context 'when there is no email address included in the omniauth hash' do
        before do
          @email = nil

          User.stub(:find_by_email).with(@email).and_return(nil)
          User.stub(:find_by_github_uid).with(@github_uid).and_return(nil)

          @user = User.find_or_create_by_email_and_github_uid(@email, @github_uid)
        end

        it 'should build a new user' do
          @user.should be_a_new_record
        end

        it 'should set the github uid of the new user to the github_uid specified' do
          @user.github_uid.should == @github_uid
        end
      end
    end
  end

  describe '#update_github_uid' do
    it 'updates the user\'s github_uid to the specified value' do
      subject.update_github_uid("12345")
      subject.github_uid.should == "12345"
    end
  end
end
