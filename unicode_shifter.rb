hash = { "à" => "&#X00E0;", "â" => "&#X00E2;", "é" => "&#X00E9;", "è" => "&#X00E8;", "ê" => "&#X00EA;", "î" => "&#X00EE;", "ô" => "&#X00F4;", "û" => "&#X00FB;", "À" => "&#X00C0;", "Â" => "&#X00C2;", "É" => "&#X00C9;", "È" => "&#X00C8;", "Ê" => "&#X00CA;", "Î" => "&#X00CE;", "Ô" => "&#X00D4;", "Û" => "&#X00DB;"}
utxt = String.new
txt = gets.chomp
txt.split("").each do |c|
  utxt += hash[c] || c
end
system "clear" or system "cls"
puts utxt
