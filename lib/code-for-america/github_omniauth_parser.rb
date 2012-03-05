class CodeForAmerica::GithubOmniAuthParser

  def initialize(github_omniauth_hash)
    @hash = github_omniauth_hash
  end

  def github_uid
    @hash.uid.to_s
  end

  def email
    @hash.info.email
  end
end
