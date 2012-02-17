require 'civic_commons/client'

class CivicCommons::TaxonomyTerm

  def initialize(taxonomy_id)
    @body = CivicCommons::Client.new.retrieve_taxonomy_term(taxonomy_id)
  end

  def get_name
    if @body.class == Hashie::Mash
      @body.name
    else
      nil
    end
  end

end
