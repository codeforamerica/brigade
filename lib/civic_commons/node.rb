require 'civic_commons/client'

class CivicCommons::Node

  def initialize(node_id)
    @body = CivicCommons::Client.new.retrieve_node(node_id)
  end

  def get_title
    if @body.class == Hashie::Mash
      @body.title
    else
      nil
    end
  end

end
