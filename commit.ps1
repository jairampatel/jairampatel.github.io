git add .
$argsList = "";
for($i = 0;$i -lt $args.count;$i++){
	$argsList += $($args[$i]);
	if($i -ne $args.count - 1){
		$argsList += " ";
	}
}
if($argsList.Length -eq 0){
    git commit -m "n/a";
}
else{
    git commit -m $($argsList)
}

git push origin master

(new-object Media.SoundPlayer "C:\WINDOWS\Media\notify.wav").play();