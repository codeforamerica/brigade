(function() {
  var NodeTypes, ParameterMissing, Utils, defaults,
    __hasProp = {}.hasOwnProperty;

  ParameterMissing = function(message) {
    this.message = message;
  };

  ParameterMissing.prototype = new Error();

  defaults = {
    prefix: "",
    default_url_options: {}
  };

  NodeTypes = {"GROUP":1,"CAT":2,"SYMBOL":3,"OR":4,"STAR":5,"LITERAL":6,"SLASH":7,"DOT":8};

  Utils = {
    serialize: function(object, prefix) {
      var element, i, key, prop, result, s, _i, _len;

      if (prefix == null) {
        prefix = null;
      }
      if (!object) {
        return "";
      }
      if (!prefix && !(this.get_object_type(object) === "object")) {
        throw new Error("Url parameters should be a javascript hash");
      }
      if (window.jQuery) {
        result = window.jQuery.param(object);
        return (!result ? "" : result);
      }
      s = [];
      switch (this.get_object_type(object)) {
        case "array":
          for (i = _i = 0, _len = object.length; _i < _len; i = ++_i) {
            element = object[i];
            s.push(this.serialize(element, prefix + "[]"));
          }
          break;
        case "object":
          for (key in object) {
            if (!__hasProp.call(object, key)) continue;
            prop = object[key];
            if (!(prop != null)) {
              continue;
            }
            if (prefix != null) {
              key = "" + prefix + "[" + key + "]";
            }
            s.push(this.serialize(prop, key));
          }
          break;
        default:
          if (object) {
            s.push("" + (encodeURIComponent(prefix.toString())) + "=" + (encodeURIComponent(object.toString())));
          }
      }
      if (!s.length) {
        return "";
      }
      return s.join("&");
    },
    clean_path: function(path) {
      var last_index;

      path = path.split("://");
      last_index = path.length - 1;
      path[last_index] = path[last_index].replace(/\/+/g, "/").replace(/.\/$/m, "");
      return path.join("://");
    },
    set_default_url_options: function(optional_parts, options) {
      var i, part, _i, _len, _results;

      _results = [];
      for (i = _i = 0, _len = optional_parts.length; _i < _len; i = ++_i) {
        part = optional_parts[i];
        if (!options.hasOwnProperty(part) && defaults.default_url_options.hasOwnProperty(part)) {
          _results.push(options[part] = defaults.default_url_options[part]);
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    },
    extract_anchor: function(options) {
      var anchor;

      anchor = "";
      if (options.hasOwnProperty("anchor")) {
        anchor = "#" + options.anchor;
        delete options.anchor;
      }
      return anchor;
    },
    extract_options: function(number_of_params, args) {
      var ret_value;

      ret_value = {};
      if (args.length > number_of_params) {
        ret_value = args.pop();
      }
      return ret_value;
    },
    path_identifier: function(object) {
      var property;

      if (object === 0) {
        return "0";
      }
      if (!object) {
        return "";
      }
      property = object;
      if (this.get_object_type(object) === "object") {
        property = object.to_param || object.id || object;
        if (this.get_object_type(property) === "function") {
          property = property.call(object);
        }
      }
      return property.toString();
    },
    clone: function(obj) {
      var attr, copy, key;

      if ((obj == null) || "object" !== this.get_object_type(obj)) {
        return obj;
      }
      copy = obj.constructor();
      for (key in obj) {
        if (!__hasProp.call(obj, key)) continue;
        attr = obj[key];
        copy[key] = attr;
      }
      return copy;
    },
    prepare_parameters: function(required_parameters, actual_parameters, options) {
      var i, result, val, _i, _len;

      result = this.clone(options) || {};
      for (i = _i = 0, _len = required_parameters.length; _i < _len; i = ++_i) {
        val = required_parameters[i];
        result[val] = actual_parameters[i];
      }
      return result;
    },
    build_path: function(required_parameters, optional_parts, route, args) {
      var anchor, opts, parameters, result, url, url_params;

      args = Array.prototype.slice.call(args);
      opts = this.extract_options(required_parameters.length, args);
      if (args.length > required_parameters.length) {
        throw new Error("Too many parameters provided for path");
      }
      parameters = this.prepare_parameters(required_parameters, args, opts);
      this.set_default_url_options(optional_parts, parameters);
      anchor = this.extract_anchor(parameters);
      result = "" + (this.get_prefix()) + (this.visit(route, parameters));
      url = Utils.clean_path("" + result);
      if ((url_params = this.serialize(parameters)).length) {
        url += "?" + url_params;
      }
      url += anchor;
      return url;
    },
    visit: function(route, parameters, optional) {
      var left, left_part, right, right_part, type, value;

      if (optional == null) {
        optional = false;
      }
      type = route[0], left = route[1], right = route[2];
      switch (type) {
        case NodeTypes.GROUP:
          return this.visit(left, parameters, true);
        case NodeTypes.STAR:
          return this.visit_globbing(left, parameters, true);
        case NodeTypes.LITERAL:
        case NodeTypes.SLASH:
        case NodeTypes.DOT:
          return left;
        case NodeTypes.CAT:
          left_part = this.visit(left, parameters, optional);
          right_part = this.visit(right, parameters, optional);
          if (optional && !(left_part && right_part)) {
            return "";
          }
          return "" + left_part + right_part;
        case NodeTypes.SYMBOL:
          value = parameters[left];
          if (value != null) {
            delete parameters[left];
            return this.path_identifier(value);
          }
          if (optional) {
            return "";
          } else {
            throw new ParameterMissing("Route parameter missing: " + left);
          }
          break;
        default:
          throw new Error("Unknown Rails node type");
      }
    },
    visit_globbing: function(route, parameters, optional) {
      var left, right, type, value;

      type = route[0], left = route[1], right = route[2];
      value = parameters[left];
      if (value == null) {
        return this.visit(route, parameters, optional);
      }
      parameters[left] = (function() {
        switch (this.get_object_type(value)) {
          case "array":
            return value.join("/");
          default:
            return value;
        }
      }).call(this);
      return this.visit(route, parameters, optional);
    },
    get_prefix: function() {
      var prefix;

      prefix = defaults.prefix;
      if (prefix !== "") {
        prefix = (prefix.match("/$") ? prefix : "" + prefix + "/");
      }
      return prefix;
    },
    _classToTypeCache: null,
    _classToType: function() {
      var name, _i, _len, _ref;

      if (this._classToTypeCache != null) {
        return this._classToTypeCache;
      }
      this._classToTypeCache = {};
      _ref = "Boolean Number String Function Array Date RegExp Undefined Null".split(" ");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        name = _ref[_i];
        this._classToTypeCache["[object " + name + "]"] = name.toLowerCase();
      }
      return this._classToTypeCache;
    },
    get_object_type: function(obj) {
      var strType;

      if (window.jQuery && (window.jQuery.type != null)) {
        return window.jQuery.type(obj);
      }
      strType = Object.prototype.toString.call(obj);
      return this._classToType()[strType] || "object";
    },
    namespace: function(root, namespaceString) {
      var current, parts;

      parts = (namespaceString ? namespaceString.split(".") : []);
      if (!parts.length) {
        return;
      }
      current = parts.shift();
      root[current] = root[current] || {};
      return Utils.namespace(root[current], parts.join("."));
    }
  };

  Utils.namespace(window, "Routes");

  window.Routes = {
// about => /about(.:format)
  about_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"about",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// activities => /activities(.:format)
  activities_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"activities",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// application => /applications/:id(.:format)
  application_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"applications",false]],[7,"/",false]],[3,"id",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// application_deployed_applications => /applications/:application_id/deployed_applications(.:format)
  application_deployed_applications_path: function(_application_id, options) {
  return Utils.build_path(["application_id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"applications",false]],[7,"/",false]],[3,"application_id",false]],[7,"/",false]],[6,"deployed_applications",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// application_locations_brigade => /brigades/:id/application_locations(.:format)
  application_locations_brigade_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"application_locations",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// applications => /applications(.:format)
  applications_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"applications",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// apps => /apps(.:format)
  apps_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"apps",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// brigade => /brigades/:id(.:format)
  brigade_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[3,"id",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// brigade_deployed_applications => /brigades/:brigade_id/deployed_applications(.:format)
  brigade_deployed_applications_path: function(_brigade_id, options) {
  return Utils.build_path(["brigade_id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[3,"brigade_id",false]],[7,"/",false]],[6,"deployed_applications",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// brigades => /brigades(.:format)
  brigades_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"brigades",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// campaigns => /campaigns(.:format)
  campaigns_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"campaigns",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// cancel_user_registration => /members/cancel(.:format)
  cancel_user_registration_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"cancel",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// captain => /captain(.:format)
  captain_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"captain",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// challenges => /challenges(.:format)
  challenges_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"challenges",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// codeacross => /codeacross(.:format)
  codeacross_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"codeacross",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// connect => /connect(.:format)
  connect_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"connect",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// deployed_application => /deployed_applications/:id(.:format)
  deployed_application_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"deployed_applications",false]],[7,"/",false]],[3,"id",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// deployed_applications => /deployed_applications(.:format)
  deployed_applications_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"deployed_applications",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// destroy_user_session => /members/sign_out(.:format)
  destroy_user_session_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"sign_out",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// edit_brigade => /brigades/:id/edit(.:format)
  edit_brigade_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// edit_home => /home/:id/edit(.:format)
  edit_home_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"home",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// edit_location => /locations/:id/edit(.:format)
  edit_location_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"locations",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// edit_user => /members/:id/edit(.:format)
  edit_user_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// edit_user_password => /members/password/edit(.:format)
  edit_user_password_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"password",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// edit_user_registration => /members/edit(.:format)
  edit_user_registration_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// error => /error(.:format)
  error_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"error",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// events => /events(.:format)
  events_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"events",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// find_brigades => /brigades/find(.:format)
  find_brigades_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[6,"find",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// find_locations => /locations/find(.:format)
  find_locations_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"locations",false]],[7,"/",false]],[6,"find",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// forums => /forums(.:format)
  forums_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"forums",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// hackforchange => /hackforchange(.:format)
  hackforchange_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"hackforchange",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// home => /home/:id(.:format)
  home_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"home",false]],[7,"/",false]],[3,"id",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// home_index => /home(.:format)
  home_index_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"home",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// join_brigade => /brigades/:id/join(.:format)
  join_brigade_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"join",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// leave_brigade => /brigades/:id/leave(.:format)
  leave_brigade_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"leave",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// location => /locations/:id(.:format)
  location_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"locations",false]],[7,"/",false]],[3,"id",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// location_deployed_applications => /locations/:location_id/deployed_applications(.:format)
  location_deployed_applications_path: function(_location_id, options) {
  return Utils.build_path(["location_id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"locations",false]],[7,"/",false]],[3,"location_id",false]],[7,"/",false]],[6,"deployed_applications",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// locations => /locations(.:format)
  locations_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"locations",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_application_deployed_application => /applications/:application_id/deployed_applications/new(.:format)
  new_application_deployed_application_path: function(_application_id, options) {
  return Utils.build_path(["application_id"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"applications",false]],[7,"/",false]],[3,"application_id",false]],[7,"/",false]],[6,"deployed_applications",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_brigade => /brigades/new(.:format)
  new_brigade_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_brigade_deployed_application => /brigades/:brigade_id/deployed_applications/new(.:format)
  new_brigade_deployed_application_path: function(_brigade_id, options) {
  return Utils.build_path(["brigade_id"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"brigades",false]],[7,"/",false]],[3,"brigade_id",false]],[7,"/",false]],[6,"deployed_applications",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_challenge => /challenges/new(.:format)
  new_challenge_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"challenges",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_deployed_application => /deployed_applications/new(.:format)
  new_deployed_application_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"deployed_applications",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_home => /home/new(.:format)
  new_home_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"home",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_location => /locations/new(.:format)
  new_location_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"locations",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_location_deployed_application => /locations/:location_id/deployed_applications/new(.:format)
  new_location_deployed_application_path: function(_location_id, options) {
  return Utils.build_path(["location_id"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"locations",false]],[7,"/",false]],[3,"location_id",false]],[7,"/",false]],[6,"deployed_applications",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_user_password => /members/password/new(.:format)
  new_user_password_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"password",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_user_registration => /members/sign_up(.:format)
  new_user_registration_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"sign_up",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// new_user_session => /members/sign_in(.:format)
  new_user_session_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"sign_in",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// not_found => /not_found(.:format)
  not_found_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"not_found",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// ogi => /ogi(.:format)
  ogi_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"ogi",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// opendata => /opendata(.:format)
  opendata_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"opendata",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// opengovernment => /opengovernment(.:format)
  opengovernment_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"opengovernment",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// openimpact => /openimpact(.:format)
  openimpact_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"openimpact",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// opensource => /opensource(.:format)
  opensource_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"opensource",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// page => /pages/*id
  page_path: function(_id, options) {
  return Utils.build_path(["id"], [], [2,[2,[2,[7,"/",false],[6,"pages",false]],[7,"/",false]],[5,[3,"id",false],false]], arguments);
  },
// pages_codeacross => /pages/codeacross(.:format)
  pages_codeacross_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"pages",false]],[7,"/",false]],[6,"codeacross",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// pages_openimpact => /pages/openimpact(.:format)
  pages_openimpact_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"pages",false]],[7,"/",false]],[6,"openimpact",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.dashboard => /admin/
  rails_admin_dashboard_path: function(options) {
  return Utils.build_path([], [], [2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]], arguments);
  },
// rails_admin.index => /admin/:model_name(.:format)
  rails_admin_index_path: function(_model_name, options) {
  return Utils.build_path(["model_name"], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.new => /admin/:model_name/new(.:format)
  rails_admin_new_path: function(_model_name, options) {
  return Utils.build_path(["model_name"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.export => /admin/:model_name/export(.:format)
  rails_admin_export_path: function(_model_name, options) {
  return Utils.build_path(["model_name"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[6,"export",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.bulk_delete => /admin/:model_name/bulk_delete(.:format)
  rails_admin_bulk_delete_path: function(_model_name, options) {
  return Utils.build_path(["model_name"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[6,"bulk_delete",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.history_index => /admin/:model_name/history(.:format)
  rails_admin_history_index_path: function(_model_name, options) {
  return Utils.build_path(["model_name"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[6,"history",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.bulk_action => /admin/:model_name/bulk_action(.:format)
  rails_admin_bulk_action_path: function(_model_name, options) {
  return Utils.build_path(["model_name"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[6,"bulk_action",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.show => /admin/:model_name/:id(.:format)
  rails_admin_show_path: function(_model_name, _id, options) {
  return Utils.build_path(["model_name","id"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[3,"id",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.edit => /admin/:model_name/:id/edit(.:format)
  rails_admin_edit_path: function(_model_name, _id, options) {
  return Utils.build_path(["model_name","id"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.delete => /admin/:model_name/:id/delete(.:format)
  rails_admin_delete_path: function(_model_name, _id, options) {
  return Utils.build_path(["model_name","id"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"delete",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.history_show => /admin/:model_name/:id/history(.:format)
  rails_admin_history_show_path: function(_model_name, _id, options) {
  return Utils.build_path(["model_name","id"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"history",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_admin.show_in_app => /admin/:model_name/:id/show_in_app(.:format)
  rails_admin_show_in_app_path: function(_model_name, _id, options) {
  return Utils.build_path(["model_name","id"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"admin",false]],[7,"/",false]],[3,"model_name",false]],[7,"/",false]],[3,"id",false]],[7,"/",false]],[6,"show_in_app",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// rails_info_properties => /rails/info/properties(.:format)
  rails_info_properties_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"rails",false]],[7,"/",false]],[6,"info",false]],[7,"/",false]],[6,"properties",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// root => /
  root_path: function(options) {
  return Utils.build_path([], [], [7,"/",false], arguments);
  },
// sign_in => /sign-in(.:format)
  sign_in_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"sign-in",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// sign_out => /sign-out(.:format)
  sign_out_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"sign-out",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// survey => /survey(.:format)
  survey_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"survey",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// tools => /tools(.:format)
  tools_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"tools",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// user => /members/:id(.:format)
  user_path: function(_id, options) {
  return Utils.build_path(["id"], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[3,"id",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// user_omniauth_authorize => /members/auth/:provider(.:format)
  user_omniauth_authorize_path: function(_provider, options) {
  return Utils.build_path(["provider"], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"auth",false]],[7,"/",false]],[3,"provider",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// user_omniauth_callback => /members/auth/:action/callback(.:format)
  user_omniauth_callback_path: function(_action, options) {
  return Utils.build_path(["action"], ["format"], [2,[2,[2,[2,[2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"auth",false]],[7,"/",false]],[3,"action",false]],[7,"/",false]],[6,"callback",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// user_password => /members/password(.:format)
  user_password_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"password",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// user_registration => /members(.:format)
  user_registration_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"members",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// user_session => /members/sign_in(.:format)
  user_session_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"members",false]],[7,"/",false]],[6,"sign_in",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// users => /members(.:format)
  users_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[7,"/",false],[6,"members",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// users_edit => /users/edit(.:format)
  users_edit_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"users",false]],[7,"/",false]],[6,"edit",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// users_password_new => /users/password/new(.:format)
  users_password_new_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[2,[2,[7,"/",false],[6,"users",false]],[7,"/",false]],[6,"password",false]],[7,"/",false]],[6,"new",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// users_sign_in => /users/sign_in(.:format)
  users_sign_in_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"users",false]],[7,"/",false]],[6,"sign_in",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// users_sign_out => /users/sign_out(.:format)
  users_sign_out_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"users",false]],[7,"/",false]],[6,"sign_out",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  },
// users_sign_up => /users/sign_up(.:format)
  users_sign_up_path: function(options) {
  return Utils.build_path([], ["format"], [2,[2,[2,[2,[7,"/",false],[6,"users",false]],[7,"/",false]],[6,"sign_up",false]],[1,[2,[8,".",false],[3,"format",false]],false]], arguments);
  }}
;

  window.Routes.options = defaults;

}).call(this);
