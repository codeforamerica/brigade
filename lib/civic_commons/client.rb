module CivicCommons
  class Client

    def initialize
      @conn = Faraday.new 'http://civiccommons.org/api/v1' do |builder|

        # Uncomment if want to log to stdout
        # builder.response :logger

        builder.use Faraday::Response::Mashify
        builder.use FaradayMiddleware::ParseJson, :content_type => /\bjson$/
        builder.use Faraday::Adapter::NetHttp
      end
    end

    def retrieve_node(node_id)
      resp = @conn.get "node/#{node_id}.json"

      resp.body
    end

    def retrieve_taxonomy_term(taxonomy_id)
       resp = @conn.get "taxonomy_term/#{taxonomy_id}.json"

       resp.body
    end
  end
end
