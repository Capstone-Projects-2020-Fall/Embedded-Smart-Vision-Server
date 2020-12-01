from application import db, create_app
app, socket_io = create_app()
app.app_context().push()
db.create_all()