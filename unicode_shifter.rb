hash = { "à" => "&#xe0;", "â" => "&#xe2;", "é" => "&#xe9;", "è" => "&#xe8;", "ê" => "&#xea;", "î" => "&#xee;", "ô" => "&#xf4;", "û" => "&#xfb;", "À" => "&#xc0;", "Â" => "&#xc2;", "É" => "&#xc9;", "È" => "&#xc8;", "Ê" => "&#xca;", "Î" => "&#xce;", "Ô" => "&#xd4;", "Û" => "&#xdb;"}
utxt = String.new
txt = gets.chomp
txt.split("").each do |c|
  utxt += hash[c] || c
end
system "clear" or system "cls"
puts utxt
