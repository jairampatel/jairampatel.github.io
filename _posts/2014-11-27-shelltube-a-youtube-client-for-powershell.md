---
layout: post
title: "Shelltube, a youtube client for Powershell"
---

With the addition of this post, 67% of my blog posts will have been about Powershell. I should probably diversify my projects a bit.

Shelltube is a Youtube client for Powershell. Just type what video you want to listen/watch and Shelltube will play it for you.

**How it works**

In version 1.0, Shelltube will launch Internet Explorer (sorry, it was the common denominator among Windows users). Although the default setting is to display the window, the user will have the option of hiding the Internet Explorer window.
The client will call the Youtube API in order to retrieve the results of the search query the user entered. At this point, the user can select which video to watch. Selecting a video will navigate the Internet Explorer window to the Youtube video url.

**Future versions**

* Have the ability to view more than 10 search results
* Remove Internet Explorer dependency. Stream directly from Youtube

