class Router(object):
    """
    Determine how to route database calls for an app's models (in this case, for an app named lims).
    All other models will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    https://strongarm.io/blog/multiple-databases-in-django/
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on lims app models to `lims_db`."""
        if model._meta.app_label == 'lims':
            return 'lims_db'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on lims app models to `lims_db`."""
        if model._meta.app_label == 'lims':
            return 'lims_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the lims app.
        if obj1._meta.app_label == 'lims' and obj2._meta.app_label == 'lims':
            return True
        # No opinion if neither object is in the lims app (defer to default or other routers).
        elif 'lims' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the lims app and the other isn't.
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the lims app's models get created on the right database."""
        if app_label == 'lims':
            # The lims app should be migrated only on the lims_db database.
            return db == 'lims_db'
        elif db == 'lims_db':
            # Ensure that all other apps don't get migrated on the lims_db database.
            return False

        # No opinion for all other scenarios
        return None
