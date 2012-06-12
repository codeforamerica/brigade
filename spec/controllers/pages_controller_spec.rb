require 'spec_helper'

describe HighVoltage::PagesController do

  describe "GET 'pages/about'" do
    it "returns http success" do
      get :show, :id => 'about'
      response.should be_success
    end
  end

end
