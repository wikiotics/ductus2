MVP design definition
=====================

Below is a cleaned up definition of what we intend to build into our MVP (Minimum Valuable Product) with a view to take a fresh start towards a new ductus platform that will make better use of current web and mobile technologies.

This is all based on private emails exchanged between the wikiotics core members.

One liner
---------
A pastebin-like site for collaborative language-education podcasts

The longer story
----------------

We build a wiki-style system for podcasts which will be very similar to the ones we currently have on ductus. Podcasts will be the first type of lessons to go into the wiki, but obviously the aim is to make it possible to create more lesson types down the road (and this must be fairly easy to do).

A podcast will be used as a language lesson (but could be about anything else, in fact) and feature:
  * a title and/or description of its content (free text)
  * tags describing which language it is teaching, using which other language.
  * a series of phrases in text form and an associated audio recording. Let's call each of them a line. Each line has a speaker defined by their name (mainly so the text representation makes sense to the reader), and a language tag.
  * a compiled version of the audio made available for download, or listened to online
  * for the purpose of making the UI a bit nicer, we allow adding a (small) picture to a podcast (which ideally is related to the lesson's content), so that it can be shown in a list of lessons.
  * audio for a line can be uploaded from a local file, or recorded online (if HTML5 recording works in the user's browser)
  * each audio bit can be listened to online separately. Downloading each bit is outside MVP scope.

For the purpose of the MVP, we don't provide any connection between different lessons. We still make it possible to fork a lesson (ie: build a new lesson using the current one as starting point). Each revision is of course saved. Functions beyond this (diff/merge) are beyond MVP scope :)

Urls
____

They are hashes, both for revisions and lessons.
  * lesson: wikiotics.org/wiki/aabbccddee
  * revision: wikiotics.org/revs/abcdefabdc

Accessing content
_________________

we provide a list of all lessons on the site. It can be customised for logged in users, restricting the list to languages they're interested in.

Users
_____

Login is not mandatory. For now, creating an account will associate a user's login to each of their contributions. Anonymous contributions will be linked to the author's IP address. We also record languages known and learnt for each user, so as to be able to give them a list of relevant content. Keep in mind that we'll want progress tracking at some point in time.

We also provide a user and group write-protected sections, publicly readable, but only editable by their owners. Content can be forked to build upon under a different url.

other stuff
___________

A few very simple static pages like /about, /privacy_policy...
The main page needs discussing, but we can start with a simple "static" teaser page.

Licensing
_________

We automatically make every contribution CC-BY-SA for now. We can discuss changing this in the future if it becomes a need.

UI
__

I won't try to decide how things look for now, but just describe what is available on each page.
For podcasts, we show roughly what ductus1 shows. The top of the page shows the title/description, maybe the picture, followed by the podcast listen/download stuff. Below the text content.
I'd love to have a very simple in-place edit system, i.e. instead of reloading a full page to edit the podcast, we find some nice shortcut like a double click, which switches a line to edit mode. In edit mode, the display is modifed to visually separate the row being edited, maybe adding a box around it. Both the audio and text can be changed in one go. Then save/cancel. Upon saving, a podcast compilation is queued (this needs some smart way of delaying compilation start and/or cancelling previously queued jobs not to overload the server).
I'm hoping we could make lesson editing more user friendly by making it look as close as possible to the view-mode. My thinking here is that users should understand more easily how the podcast works if it always looks virtually the same. Also, avoiding a full page reload means faster interaction, so users will do it more happily. We drop log messages, as we can add them later on if needed.

Login page can be the default django login page for now.

the tech stuff
--------------

  * each lesson is exchanged as JSON between client and server. The UI side modifies the lesson object, which will auto-send itself to the server as needed, thanks to backbone magic. The server validates and stores the JSON object, and possibly runs a few triggers upon saving (like rebuilding the podcast).
  * a lesson type therefore becomes a JSON structure with storage logic, plus a server side validator (and triggers), and client side view/edit UI.
  * DB: postgreSQL. Things may be more flexible if we don't store content as json for now. We rebuild the lesson hierarchy from a podcast table + rows table. Each row (in a podcast) s connected to a lesson revision through an intermediate table which gives the order in which rows appear in the podcast.. So with a simple database join we can get a lesson's content and put that into json. Lesson attributes (title, description, author, etc...) will be stored in separate db fields, and we'll translate the object to JSON for talking to the client. This allows finer querying (later).
  * indexing lesson content: google will do that very well for now
  * format(s) for audio will (likely) be mp4 and vorbis.

techier stuff
-------------

server-side
___________

 * we build an MVC for each lesson type, plus a parent one, something like WikiPageModel/View/Controller and the same for each type derived from it.
 * the WikiPage would deal with all revisioning, authorship, anything common to all lesson types.
 * PodcastModel/View/Controller deals with the rest, ie: stuff specific to this type. We only need a view that sends the JSON object to the client, and something to edit it.
 * media storage: we'll look at using media storage provided by Django, or fallback to ductus1 media storage system.
 * unit tests: we'll use pytest-django

client-side
___________

 * we'd have an MV* for the lesson, say WikiPageModel and WikiPageView for the logic common to all lesson types
 * PodcastModel and PodcastView would derive from the above. Same logic as server side.
 * and for the rest, we'll just play by ear as we go
