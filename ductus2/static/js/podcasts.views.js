// views populated from models/collections by Marionette

var PodcastListItemView = Backbone.Marionette.ItemView.extend({
    template: '#podcast-item-view',
    tagName: 'li'
});

var PodcastListView = Backbone.Marionette.CompositeView.extend({
    itemViewContainer: '#podcast-list',
    itemView: PodcastListItemView,
    template: '#podcast-list-view'
});
