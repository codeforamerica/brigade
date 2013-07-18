require 'spec_helper'

describe UsersController, :focus do
  describe 'DELETE destroy' do 
    before :each do 
      @user = FactoryGirl.create(:user)
      sign_in :user, @user
    end 
    
    it "deletes the user" do 
      expect{ 
        delete :destroy, id: @user 
      }.to change(User,:count).by(-1) 
    end 
    it "redirects to index" do 
      delete :destroy, id: @user 
      response.should redirect_to root_path 
    end 
    
    describe "another user" do
      before :each do 
        @another_user = FactoryGirl.create(:user)
      end
      it "cannot be destroyed" do
        expect{ 
          delete :destroy, id: @another_user 
        }.to_not change(User,:count).by(-1) 
      end
    end
  end
  
end