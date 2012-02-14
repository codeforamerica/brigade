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
end
