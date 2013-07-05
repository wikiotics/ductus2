// main podcast model

var User = Backbone.Model.extend({
    /*
    * id: the django id, null for anonymous users
    * login: ...
    * email: ...
    */
    defaults: {
        id: null,
        login: 'anonymous',
        email: ''
    }
});
var Podcast = Backbone.Model.extend({
    /*
    * properties:
    * id: same as the django id
    * title: text, limited to 512 chars
    * description: a longer text
    * author: a user model
    * timestamp: when the current revision was created
    * rows: we're cheating here, the backend sends a string, we hack it into proper json like:
        [
            {"text": a string, "audio": a ref to some audio file},
            (...)
        ]
    */

    defaults: {
        title: '',
        description: ''
    },

    initialize: function(options) {
        // options contains the JSON received from the API
        //console.log('creating Podcast object', this, options);
    }
});
var PodcastList = Backbone.Collection.extend({
    model: Podcast,
    url: '/api/podcasts/'
});

