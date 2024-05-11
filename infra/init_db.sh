aerich init -t app.database.TORTOISE_ORM
aerich init-db

# Remove database
# docker colume ls | grep carlemany-backend-data | awk '{ print $2}' | xargs docker volume rm