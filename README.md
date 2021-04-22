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

-(https://tipsy-backend.herokuapp.com/venue_posts/) - This is the endpoint for the list of venue posts (comments/pics left on a venue's page). 

-(https://tipsy-backend.herokuapp.com/venue_posts/<uuid:pk>/) - This is the endpoint for the venue post detail page- a specific comment/image left on a venue's page. 

-(https://tipsy-backend.herokuapp.com/posts/) - This is the endpoint for the list of user posts (comments/pics left on a user's page). 

-(https://tipsy-backend.herokuapp.com/posts/<uuid:pk>/) - This is the endpoint for the user post detail page- a specific comment/image left on a user's page. 

## To **follow** another user or venue:
1. You must be logged in as a user.
2. Send a PUT request to the detail page of the user/venue you want to follow (eg : /venues/10c56a24-0509-4cc8-90ee-b898f0a02b63/). If the user doesn't follow this user/venue, you will get a response that says "user/venue followed", and that user will show up on the user/venues list of followers, and the user/venue will show up on that user's 'following' list. If the user already follows that user/venue, the PUT request will generate a response that the user/venue has been unfollowed (and remove everything from relevant lists of followers/following).

# Posts and Venue Posts#
1. First of all, I (Ben) haven't troubleshot whether you can post as a user through API requests yet- I've only been doing it as the admin. That will hopefully be working by tonight (4/22).
2. Right now, each post/venue post links to the user who posted them and the venue/user on which they were posted, but they don't automatically populate on that user/venue's detail page- working on that tonight as well. 

## To **like** a post or venue_post:
1. This is the same method as 'following' above: As a logged in user, send a 'Put' request to a post or venue post's unique url. If you haven't liked that post, you will get a response saying you liked it- if you already like it, the response will tell you that you UnLiked it. 
