module CustomMatchers
  class BeWellFormed
    def matches?(files)
      @error_messages = []
      files.each do |filename|
        begin
          @error_messages << check_for_tab_characters(filename)
          @error_messages << check_for_extra_spaces(filename)
        rescue
        end
      end
      @error_messages.compact!.empty?
    end

    def failure_message_for_should
      @error_messages.join("\n")
    end

    private

    def check_for_tab_characters(filename)
      failing_lines = []
      File.readlines(filename).each_with_index do |line,number|
        failing_lines << number + 1 if line =~ /\t/
      end

      unless failing_lines.empty?
        "#{filename} has tab characters on lines #{failing_lines.join(', ')}"
      end
    end

    def check_for_extra_spaces(filename)
      failing_lines = []
      File.readlines(filename).each_with_index do |line,number|
        next if line =~ /^\s+#.*\s+\n$/
        failing_lines << number + 1 if line =~ /\s+\n$/
      end

      unless failing_lines.empty?
        "#{filename} has spaces on the EOL on lines #{failing_lines.join(', ')}"
      end
    end
  end

  def be_well_formed
    BeWellFormed.new
  end
end
