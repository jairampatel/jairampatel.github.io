---
layout: post
title: "Installing Arch Linux on my CR-48"
---

CR-48 is the beta Chromebook released by Google several years ago. It was given away for free to those who applied/were selected. I consider myself extremely fortunate for having been selected and I tried to make the most of it.

If you’re not aware, Chromebooks run on Chrome OS, which is essentially just the Chrome browser. It is built upon a Linux kernel so if you were to flip the hardware switch to developer mode (as I did multiple times), you would be able to use the shell and gain more control over your Chromebook.

One of the reasons I installed Arch was because I wanted a desktop. Also, I was a long-time Ubuntu user and wanted to try something new. Don’t get me wrong, the Chromebook was fantastic. The time it took to turn on my Chromebook and start browsing the web was generally around 10 seconds. But since the CR-48 was primarily a browser, it made other tasks such as ssh/git/writing code a bit harder. Granted, you could drop into developer mode, ssh into your server and be good to go. However, I also wanted to tinker with my laptop a bit.

The way the CR-48 is set up is that it has 3 kernel/rootfs partitions. The 1st and 2nd pair are used by you/updating the Chromebook. The 3rd pair is a spare

First, I tried installing Arch using this method:

<blockquote>
	<p>
		https://sites.google.com/a/chromium.org/dev/chromium-os/developer-information-for-chrome-os-devices/cr-48-chrome-notebook-developer-information/how-to-boot-ubuntu-on-a-cr-48
	</p>
</blockquote>
This method installed Arch to the 3rd pair, keeping Chrome OS on the 1st two pairs. However, I ran into issues where my modules were not being loaded correctly. Instead, I decided to completely overwrite all the partitions and have Arch Linux use the entire disk.

In order to achieve this, I needed to open up my CR-48, disable the BIOS write protection, and flash a new BIOS. This was pretty straight forward. The following took care of these steps:

<blockquote>
	<p>
		http://cr-48.wikispaces.com/Open+the+Cr-48
	</p>
	<p>
		http://cr-48.wikispaces.com/Flash+BIOS
	</p>
</blockquote>
After that, I created a bootable USB with Arch Linux on it, plugged it into my CR-48, and installed Arch.

I’ve only spent a few days using Arch but so far, I love it. I am able to choose which packages to install from the very beginning. Because of this, I’m able to minimize the amount of space I’m using as well as have more control over my system.

One thing I did notice was that using Firefox/Chromium on Arch was a little bit slower than using Chrome on Chrome OS. However, all of the other features that Arch offers far outweigh this minor inconvenience.
