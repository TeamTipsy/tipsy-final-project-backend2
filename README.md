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

