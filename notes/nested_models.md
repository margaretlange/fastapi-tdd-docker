https://dev.to/jamesbmour/fastapi-part-2-routing-path-parameters-and-query-parameters-3ig8

Prompt

Write me a example of a fastapi REST CRUD api with nested resources.
The resources should be:
- user
- item
such that a user can have many items but an item only has one user.

Write async CRUD (Create, read ("get"), update, and delete) api endpoints for both items and users. The "get" endpoint for the "item" resource should return some kind of user id for the user who owns the item, in addition to other item information.  Validate payload and response with the pydantic library.

The supporting backend should be a sql database, and managed via the tortoise orm. Users-to-items should be represented as one-to-many in the database structure.

##
okay that was helpful
can i add auth0 support? I think i need to look at auth0 example
