# Team Tipsy - End Points Documentation
##(https://tipsy-backend.herokuapp.com/admin) - for access to django admin
---
### Current URLs:

**Remember, if adding JSON data using Insomnia, to use " instead of '.**


-Create a user: (https://tipsy-backend.herokuapp.com/auth/users/)
    **REQUIRED FIELDS**
    username, password, email 

-Get token: (https://tipsy-backend.herokuapp.com/auth/token/login/)

-(https://tipsy-backend.herokuapp.com/users/<uuid:pk>/) - This is the endpoint for a users 'profile' page. 

-(https://tipsy-backend.herokuapp.com/venues/) - This is the endpoint for the list of venues. 

-(https://tipsy-backend.herokuapp.com/venues/<uuid:pk>/) - This is the endpoint for the venue detail page. 

## To 'follow another user or venue:
1. You must be logged in as a user.
2. Send a PUT request to the detail page of the user/venue you want to follow (eg : /venues/10c56a24-0509-4cc8-90ee-b898f0a02b63/). If the user doesn't follow this user/venue, you will get a response that says "user/venue followed", and that user will show up on the user/venues list of followers, and the user/venue will show up on that user's 'following' list. If the user already follows that user/venue, the PUT request will generate a response that the user/venue has been unfollowed (and remove everything from relevant lists of followers/following).
