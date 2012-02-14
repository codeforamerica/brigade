require 'civic_commons/node'

class CivicCommons::Application < CivicCommons::Node

  def get_short_description
    get_value_of('sdesc')
  end

  def get_description
    get_value_of('description')
  end

  def get_creator_nid
    get_node_attribute_nid('creator')
  end

  def get_license_tid
    get_node_attribute_tid('license')
  end

  private

  def get_node_attribute(attribute_name)
    @body.send(:[], "field_application_#{attribute_name}").und[0]
  end

  def get_value_of(name)
    execute do
      get_node_attribute(name).value
    end
  end

  def get_node_attribute_nid(name)
    execute do
      get_node_attribute(name).nid
    end
  end

  def get_node_attribute_tid(name)
    execute do
      get_node_attribute(name).tid
    end
  end

  def execute(&block)
    begin
      yield
    rescue
      nil
    end
  end

end
