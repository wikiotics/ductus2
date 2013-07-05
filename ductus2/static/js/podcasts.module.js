// The podcast management module
// we'll probably have to split it later on, but for now, we just dump everything podcast-related in it

d2_app.module('PodcastModule', function(PodcastModule, d2_app, Backbone, Marionette, $, _) {

    PodcastModule.addInitializer(function () {

        this.podcast_list = new PodcastList;
        this.podcast_list.fetch({reset: true});

        var podcastListView = new PodcastListView({
            collection: this.podcast_list
        });
        d2_app.mainRegion.show(podcastListView);
    });

});
