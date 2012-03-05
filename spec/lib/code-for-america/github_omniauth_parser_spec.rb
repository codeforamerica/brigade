require 'code-for-america/github_omniauth_parser'

describe CodeForAmerica::GithubOmniAuthParser do
  subject { CodeForAmerica::GithubOmniAuthParser.new(OmniAuth::AuthHash.new({ 'provider'=>'github', 'uid'=>1489336, 'info'=> { 'email'=>'test@example.com'} })) }

  describe '#github_uid' do
    it 'returns the email contained in the github omniauth hash' do
      subject.github_uid.should == '1489336'
    end
  end

  describe '#email' do
    it 'returns the github_uid contained in the github omniauth hash' do
      subject.email.should == 'test@example.com'
    end
  end
end
