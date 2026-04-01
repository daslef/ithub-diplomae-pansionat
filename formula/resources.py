from import_export import resources

from formula.models import Room


class RoomResource(resources.ModelResource):
    class Meta:
        model = Room


class AnotherRoomResource(resources.ModelResource):
    class Meta:
        model = Room
