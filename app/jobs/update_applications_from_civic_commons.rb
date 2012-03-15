require 'civic_commons/application'
require 'civic_commons/creator'
require 'civic_commons/taxonomy_term'

class UpdateApplicationsFromCivicCommons
  def self.perform
    Application.all.each do |app|
      node_app = CivicCommons::Application.new(app.nid)

      if node_app.body
        app.name = node_app.get_title
        app.short_description = node_app.get_short_description
        app.civic_commons_description = node_app.get_description

        node_app_creator = CivicCommons::Creator.new(node_app.get_creator_nid)
        app.creator = node_app_creator.get_title

        app.license = CivicCommons::TaxonomyTerm.new(node_app.get_license_tid).get_name

        app.save
      end
    end
  end

end
