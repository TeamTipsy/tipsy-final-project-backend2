# Team Tipsy - End Points Documentation
##(https://tipsy-backend.herokuapp.com/admin) - for access to django admin
---
### Current URLs:

**Remember, if adding JSON data using Insomnia, to use " instead of '.**


-Create a user: (https://tipsy-backend.herokuapp.com/auth/users/)
    **REQUIRED FIELDS**
    username, password, email 

-Get token: (https://tipsy-backend.herokuapp.com/auth/token/login/)

- https://tipsy-backend.herokuapp.com/auth/users/me/  - get the username, email, and user_id of user currently logged in (requires token authentication).

-(https://tipsy-backend.herokuapp.com/users/<uuid:pk>/) - This is the endpoint for a users 'profile' page. 

-(https://tipsy-backend.herokuapp.com/venues/) - This is the endpoint for the list of venues. 

-(https://tipsy-backend.herokuapp.com/venues/<uuid:pk>/) - This is the endpoint for the venue detail page. 


-(https://tipsy-backend.herokuapp.com/posts/) - This is the endpoint for the list of user posts (comments/pics left on a user's page). 

-(https://tipsy-backend.herokuapp.com/posts/<uuid:pk>/) - This is the endpoint for the user post detail page- a specific comment/image left on a user's page. 

## To **follow** another user or venue:
1. You must be logged in as a user.
2. Send a PUT request to the detail page of the user/venue you want to follow (eg : /venues/10c56a24-0509-4cc8-90ee-b898f0a02b63/). If the user doesn't follow this user/venue, you will get a response that says "user/venue followed", and that user will show up on the user/venues list of followers, and the user/venue will show up on that user's 'following' list. If the user already follows that user/venue, the PUT request will generate a response that the user/venue has been unfollowed (and remove everything from relevant lists of followers/following).

# Posts 
1. To post: send a POST request to the /posts/ endpoint. You must be logged in to do this, and you must EITHER provide a "posted_to_venue":"<uuid:pk>" OR "posted_to_user":"<uuid:pk>" - this tells the database which user/venue profile you're posting on. You must provide post_img OR post_text OR both. If you don't do these things, you won't get a nice error message- instead you'll probably get a weird page response where you were expecting JSON. I'm working on making response error messages to explain what is needed from sender. 
2. To EDIT or DELETE a post or venue: Send a PATCH or DELETE request to the /posts/<uuid:pk> endpoint or venues/<uuid:pk> . This only works if you are logged in as the user who added the post or venue.
3. You can also "Post" a new venue as a user: You send a POST request to the /venues/ endpoint. The only required field is a venue_name. 
4. Venues render with "posted_to_venue"- that's all the posts that have been left on that venue's page. Users render with "posted_to_user" and "posts_by"- the first is post's that have been left on their page, the second is posts they have made. 

## To **like** a post:
1. This is the same method as 'following' above: As a logged in user, send a 'Put' request to a post's unique url. If you haven't liked that post, you will get a response saying you liked it- if you already like it, the response will tell you that you UnLiked it. 
