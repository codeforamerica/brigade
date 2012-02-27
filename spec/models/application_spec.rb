require 'spec_helper'

describe Application do
  subject { Factory(:application) }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end

  it 'should be invalid without a nid' do
    subject.nid = nil
    subject.should_not be_valid
  end

  it 'should be valid with a repository url' do
    subject.repository_url = 'https://github.com/wearetitans/code-for-america'
    subject.should be_valid
  end

  it 'should be valid with a irc channel' do
    subject.irc_channel = '#some-channel'
    subject.should be_valid
  end

  it 'should be valid with a twitter hashtag' do
    subject.twitter_hashtag = '#brigade-hashtag'
    subject.should be_valid
  end

  it 'should be valid with a description' do
    subject.description = 'Long winded description'
    subject.should be_valid
  end

  it 'should be valid with a video embed code' do
    subject.video_embed_code = '<iframe width="560" height="315" src="http://www.youtube.com/embed/qkceyKlYrJo" frameborder="0" allowfullscreen></iframe>'
    subject.should be_valid
  end

  context 'pictures' do

    before do
      VCR.use_cassette(:s3_file_save) { @app_with_pics = FactoryGirl.create(:application_with_four_pictures) }
    end

    it 'should be valid with multiple pictures' do
      @app_with_pics.should be_valid
    end

    it 'should not be valid with more than four pictures' do
      VCR.use_cassette(:s3_file_save) { @app_with_pics.pictures.create(file: File.open("#{Rails.root}/app/assets/images/rails.png")) }
      @app_with_pics.should_not be_valid
    end
  end
end
